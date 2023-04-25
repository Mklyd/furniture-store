from django.db import models


class NavMenu(models.Model):
    CHOICES = (
        ('upholstered_furniture', 'мягкая мебель'),
        ('mirrors', 'Зеркала'),
        ('dressers_and_cabinets', 'Комоды и тумбы'),
        ('dining_sets', 'Обеденные группы'),
        ('entryways', 'Прихожие'),
        ('wardrobes', 'Шкафы'),
        ('kitchens', 'Кухни'),
        ('accessories', 'Акссесуары'),
        ('mattresses', 'Матрасы'),
        ('bedrooms', 'Спальни')
    )
    name = models.CharField( max_length=255, choices=CHOICES, unique=True)

    def __str__(self):
        return self.get_name_display()

class Category(models.Model):
    name_category = models.CharField(max_length=50, verbose_name='Категория', unique=True)
    menu_item = models.ForeignKey(NavMenu, on_delete=models.CASCADE, verbose_name='меню', null=True, blank=True, related_name='categories')

    class Meta:
        verbose_name_plural = 'Категории'
        verbose_name = 'Категория'

    def __str__(self) -> str:
        return self.name_category


class Subcategory(models.Model):
    name = models.CharField(max_length=50, verbose_name='Подкатегория', unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories', verbose_name='Категория')

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
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='Имя продукта')
    images = models.ManyToManyField('Image', blank=True, verbose_name='Фото товара')
    description = models.TextField(verbose_name='Описание')
    short_description = models.CharField(max_length=250 ,verbose_name='Короткое описание')
    quantity = models.IntegerField(verbose_name='Количество')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,  blank=True, verbose_name='Категория')
    subcategory = models.ManyToManyField(Subcategory,related_name='subcategory_model', blank=True, verbose_name='Подкатегория')
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


class CollectionProduct(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя коллекции')
    short_description = models.TextField(verbose_name='Короткое описание')
    description = models.TextField(verbose_name='Описание')

    class Meta:
        verbose_name_plural = 'Коллекции'
        verbose_name = 'Коллекция'

    def __str__(self) -> str:
        return self.name
