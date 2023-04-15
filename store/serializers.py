from rest_framework import serializers

from .models import Product, Subcategory



class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('name',)

class ProductSerializer(serializers.ModelSerializer):
    subcategory = SubcategorySerializer(many=True, read_only=True)
    class Meta:
        model = Product
        fields = ['name' ,
    'images' ,
    'description' ,
    'short_description' ,
    'quantity' ,
    'category' ,
    'subcategory' ,
    'price',
    
    'sale',
    'sku',
    'width' ,
    'height',
    'country' ,
    'frame_composition',
    'legs_composition' ,
    'upholstery_composition']