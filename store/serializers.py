from rest_framework import serializers

from .models import Product, Category, Subcategory, Image, CollectionProduct

class CollectionProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionProduct
        fields = ('id', 'image')

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image')


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = ('id', 'name')

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True, read_only=True)
    
    class Meta:
        model = Category
        fields = ('id', 'name', 'subcategories')



class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
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