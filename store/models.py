from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import GenericForeignKey


class NavMenu(models.Model):
    CHOICES = (
        ('upholstered_furniture', 'Мягкая мебель'),
        ('mirrors', 'Зеркала'),
        ('dressers_and_cabinets', 'Комоды и тумбы'),
        ('dining_sets', 'Обеденные группы'),
        ('entryways', 'Прихожие'),
        ('wardrobes', 'Шкафы'),
        ('kitchens', 'Кухни'),
        ('accessories', 'Акссесуары'),
        ('mattresses', 'Матрасы'),
        ('bedrooms', 'Спальни'),
        ('beds', 'Кровати'),
    )
    name = models.CharField( max_length=255, choices=CHOICES, unique=True, verbose_name='Имя пункта меню')
    show_menu = models.BooleanField(default=True, verbose_name='Включить в меню')
    show_catalog = models.BooleanField(default=True, verbose_name='Включить в каталог')


    class Meta:
        verbose_name_plural = 'Меню'
        verbose_name = 'Меню'

    def __str__(self):
        return self.get_name_display()


class Category(models.Model):
    image = models.ImageField(upload_to='products/category', null=True,verbose_name='Изображение категории', blank=False)
    name_category = models.CharField(max_length=255, verbose_name='Категория', unique=True, blank=False)
    menu_item = models.ForeignKey(NavMenu, on_delete=models.CASCADE, verbose_name='Относится к пункту меню', null=True, blank=False, related_name='categories')

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'

    def __str__(self) -> str:
        return self.name_category


class Subcategory(models.Model):
    name = models.CharField(max_length=50, verbose_name='Подкатегория', unique=True, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories', verbose_name='Категория')

    class Meta:
        verbose_name_plural = 'Подкатегории'
        verbose_name = 'Подкатегория'

    def __str__(self):
        return self.name

class ImageCollection(models.Model):
    image = models.ImageField(upload_to='products/collection_product', null=True, blank=True, verbose_name='Изображение коллекции')

    class Meta:
        verbose_name_plural = 'Фото коллекции'
        verbose_name = 'Фото коллекции'
    
    def __str__(self):
        return self.image.url
    
    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" style="width: 105px; height:105px;" />' % self.image.url)
        else:
            return 'No Image Found'

    image_tag.short_description = 'Image'


class ImageProduct(models.Model):
    image = models.ImageField(upload_to='products', null=True, blank=True, verbose_name='Изображение товара')

    class Meta:
        verbose_name_plural = 'Изображение товаров'
        verbose_name = 'Изображение товара'

    def __str__(self):
        return self.image.url
    
    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" style="width: 105px; height:105px;" />' % self.image.url)
        else:
            return 'No Image Found'

    image_tag.short_description = 'Image'


class DetailProductModelBase(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя поля')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(default=0)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        verbose_name_plural = 'Фото товаров'
        verbose_name = 'Фото товара'
        abstract = True


class DetailProductModel(DetailProductModelBase):
    detail = models.TextField(verbose_name='Материал', null=True)

    class Meta:
        verbose_name = 'элемент деталей'
        verbose_name_plural = 'Детали'

class CollectionProduct(models.Model):
    images = models.ManyToManyField(ImageCollection, null=True, verbose_name='Изображение коллекции', blank=False)
    name = models.CharField(max_length=255, verbose_name='Имя коллекции', blank=False)
    short_description = models.CharField(max_length=255, verbose_name='Новинка', blank=True)
    description = models.TextField(verbose_name='Описание', blank=False)

    class Meta:
        verbose_name_plural = 'Коллекции'
        verbose_name = 'Коллекция'

    def __str__(self) -> str:
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя продукта', blank=False)
    images = models.ManyToManyField('ImageProduct', verbose_name='Фото товара', blank=False)
    description = models.TextField(verbose_name='Описание', blank=False)
    short_description = models.CharField(max_length=250 ,verbose_name='Короткое описание', blank=False)
    quantity = models.PositiveSmallIntegerField(verbose_name='Количество', default=0, blank=False)
    collection = models.ForeignKey(CollectionProduct, on_delete=models.CASCADE, blank=False, null=True, verbose_name='Коллекция')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,  blank=False, verbose_name='Категория')
    subcategory = models.ManyToManyField(Subcategory,related_name='subcategory_model', blank=True, verbose_name='Подкатегория')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена', blank=False)
    slug = models.SlugField()
    sale = models.PositiveSmallIntegerField(default=0,blank=True, verbose_name='Скидка')
    sku = models.CharField(max_length=50, verbose_name='Артикул', null=True, blank=False)
    width = models.PositiveSmallIntegerField(verbose_name='Ширина, см', null=True, blank=False)
    height = models.PositiveSmallIntegerField(verbose_name='Высота, см', null=True, blank=False)
    country = models.CharField(max_length=50, verbose_name='Страна', null=True, blank=False)
    material = models.CharField(max_length=100, verbose_name='Материал', null=True, blank=False)
    color = models.CharField(max_length=50, verbose_name='Цвет', null=True, blank=False)
    style = models.CharField(max_length=50, verbose_name='Стиль', null=True, blank=False)
    details = GenericRelation(DetailProductModel, null=True)
    date = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True, null=True)

    class Meta:
        verbose_name_plural = 'Товары'
        verbose_name = 'Товар'

    def __str__(self) -> str:
        return self.name
    
    def delete(self, *args, **kwargs):
            # Delete associated images from the filesystem
            for image in self.images.all():
                image.image.delete()
            
            # Call the superclass delete() method to complete the deletion process
            super().delete(*args, **kwargs)






