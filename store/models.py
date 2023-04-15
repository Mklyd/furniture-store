from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Категория',)
    
    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'

    def __str__(self) -> str:
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=50, verbose_name='Подкатегория')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')

    class Meta:
        verbose_name_plural = 'Подкатегории'
        verbose_name = 'Подкатегория'

    def __str__(self):
        return self.name
    

class Image(models.Model):
    image = models.ImageField(upload_to='products', null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Фото товаров'
        verbose_name = 'Фото товара'




class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя продукта')
    images = models.ManyToManyField('Image', blank=True, verbose_name='Фото товара')
    description = models.TextField(verbose_name='Описание')
    short_description = models.CharField(max_length=250 ,verbose_name='Короткое описание')
    quantity = models.IntegerField(verbose_name='Количество')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    subcategory = models.ManyToManyField(Subcategory,related_name='subcategory_model', verbose_name='Подкатегория')
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='Цена')
    slug = models.SlugField()
    sale = models.PositiveSmallIntegerField(verbose_name='Скидка')
    sku = models.CharField(max_length=50, verbose_name='Артикул')
    width = models.PositiveSmallIntegerField(verbose_name='Ширина, см')
    height = models.PositiveSmallIntegerField(verbose_name='Высота, см')
    country = models.CharField(max_length=50, verbose_name='Страна')
    frame_composition = models.CharField(max_length=255, null=True, blank=True, verbose_name='Состав-Каркас')
    legs_composition = models.CharField(max_length=255, null=True, blank=True, verbose_name='Состав-Ножки')
    upholstery_composition = models.CharField(max_length=255, null=True, blank=True, verbose_name='Состав-Обивка')


    class Meta:
        verbose_name_plural = 'Товары'
        verbose_name = 'Товар'

    def __str__(self) -> str:
        return self.name

