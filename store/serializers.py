from rest_framework import serializers

from .models import Product, Subcategory, Image


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image')

class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('name',)

class ProductSerializer(serializers.ModelSerializer):
    subcategory = SubcategorySerializer(many=True, read_only=True)
    images = ImageSerializer(many=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'images' ,
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