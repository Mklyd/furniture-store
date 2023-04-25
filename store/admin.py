from django.contrib import admin
from .models import Product, Category, Subcategory, Image, CollectionProduct, NavMenu
from django.contrib.admin import widgets
from django.db import models

admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Image)
admin.site.register(CollectionProduct)
admin.site.register(NavMenu)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ('name_startswith', 'category')
    list_display = ['id', 'name', 'category', 'quantity','price']
    formfield_overrides = {
        models.ManyToManyField: {'widget': widgets.FilteredSelectMultiple('элементы', False)}
    }
    
    fieldsets = (
        (
            'Товар',
            {
                'fields': ['name', 'description', 'short_description', 'images', 'quantity',( 'category', 'subcategory'), 'price', 'sale'],
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



