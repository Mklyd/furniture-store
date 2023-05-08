from rest_framework import serializers

from .models import Product, Category, Subcategory, Image, CollectionProduct, NavMenu   

class CollectionProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollectionProduct
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'image')


class SubcategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Subcategory
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'

class NavMenuSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()

    class Meta:
        model = NavMenu
        fields = '__all__'

    def get_name(self, obj):
        return dict(NavMenu.CHOICES).get(obj.name)

class AllDataSerializer(serializers.ModelSerializer):
    #categories = CategorySerializer(many=True, read_only=True)
    menu_item = NavMenuSerializer(read_only=True)
    subcategories = SubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id',  'menu_item', 'name_category','subcategories']


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    subcategory = SubcategorySerializer(many=True, read_only=True)
    images = ImageSerializer(many=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'images', 'description' , 'short_description', 'quantity', 'category', 'subcategory', 'price',
                    'sale', 'sku', 'width', 'height', 'country', 'frame_composition', 'legs_composition' , 'upholstery_composition']