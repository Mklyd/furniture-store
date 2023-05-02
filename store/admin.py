from django.contrib import admin
from .models import Product, Category, Subcategory, Image, CollectionProduct
from django.contrib.admin import widgets
from django.utils.html import mark_safe
from django.utils.html import format_html
from django.db import models

admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(CollectionProduct)


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'image_tag')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ('name_startswith', 'category')
    list_display = ['id', 'name', 'category', 'quantity','price']

    formfield_overrides = {
        models.ManyToManyField: {'widget': widgets.FilteredSelectMultiple('элементы', False)}
    }

    def image_tag(self, obj):
        return format_html('<img src="{}" style="max-height: 200px; max-width: 200px"/>'.format(obj.image.url))
    image_tag.short_description = 'Image'
    readonly_fields = ('image_tag',)

    fieldsets = (
        (
            'Товар',
            {
                'fields': ['name', 'description', 'short_description', 'quantity',( 'category', 'subcategory'), 'price', 'sale'],
            },
        ),
        (
            'Фото',
            {
                'fields': ['image_tag', 'images'],
            },
        ),
        (
            'О товаре',
            {
                'fields': ['sku', 'width', 'height', 'country'],
                
            },
            
        ),
        (
            'Детали',
            {
                'fields': ['frame_composition', 'legs_composition', 'upholstery_composition']
                
            },
            
        ),

    )
    ordering = []



