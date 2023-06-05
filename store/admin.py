from django.contrib import admin
from django.db import models
from django.utils.safestring import mark_safe
from django.contrib.admin import widgets

from .models import Product, Category, Subcategory, ImageProduct, CollectionProduct,ImageCollection, NavMenu, DetailProductModel

from django import forms

from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline



admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(NavMenu)
admin.site.register(ImageProduct)
admin.site.register(ImageCollection)


class DynamicModelForm(forms.ModelForm):
    class Meta:
        model = DetailProductModel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget = forms.TextInput()


class DynamicModelInline(GenericTabularInline):
    model = DetailProductModel
    form = DynamicModelForm


class ImageCollectionInline(admin.StackedInline):
    model = CollectionProduct.images.through
    extra = 1
    verbose_name = 'Изображение коллекции'
    verbose_name_plural = 'Изображения коллекции'


@admin.register(CollectionProduct)
class CollectionProductAdmin(admin.ModelAdmin):
    fieldsets = (
        (
            'Товар',
            {
                'fields': ['name', 'description', 'short_description'],
            },
        ),
    )
    inlines = [ImageCollectionInline]


class ImageInline(admin.TabularInline):
    model = Product.images.through
    extra = 1
    verbose_name = 'Изображение товара'
    verbose_name_plural = 'Изображения товаров'



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ('name',    )
    list_display = ['id', 'name', 'category', 'quantity','price', 'image_tag']

    def image_tag(self, obj):
        return mark_safe('<img src="{}" width="50" height="50" />'.format(obj.images.first().image.url))
    image_tag.short_description = 'Image'

    formfield_overrides = {
        models.ManyToManyField: {'widget': widgets.FilteredSelectMultiple('элементы', False)},
    }
    fieldsets = (
        (
            'Товар',
            {
                'fields': ['name', 'description', 'short_description', 'quantity', 'collection', ( 'category', 'subcategory'), 'price', 'sale'],
            },
        ),
        (
            'О Товаре',
            {
                'fields': ['sku', 'width', 'height', 'country', 'material', 'color', 'style',]
            }
        )
    )

    inlines = [ImageInline ,DynamicModelInline]
