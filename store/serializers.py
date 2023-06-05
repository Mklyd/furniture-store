from rest_framework import serializers

from .models import Product, Category, Subcategory, ImageProduct, CollectionProduct, ImageCollection ,NavMenu, DetailProductModel

class ImageCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageCollection
        fields = ('id', 'image')

class CollectionProductSerializer(serializers.ModelSerializer):
    images = ImageCollectionSerializer(many=True)

    class Meta:
        model = CollectionProduct
        fields = ['id', 'name', 'short_description', 'description', 'images']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageProduct
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

class DetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DetailProductModel
        fields = ['id', 'name', 'detail']

        
class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    subcategory = SubcategorySerializer(many=True, read_only=True)
    images = ImageSerializer(many=True)
    collection=CollectionProductSerializer()
    about_product = serializers.SerializerMethodField()
    details = serializers.SerializerMethodField()
    class Meta:
        model = Product
        fields = ['id', 'name', 'images', 'description' , 'short_description', 'quantity','collection' , 'category', 'subcategory', 'price',
                    'sale', 'about_product', 'details', 'date'] 
        
    def get_about_product(self, obj):
        about_product = {
            'sku': obj.sku,
            'width': obj.width,
            'height': obj.height,
            'country': obj.country,
            'material': obj.material,
            'color': obj.color,
            'style': obj.style,
        }
        return about_product

    def get_details(self, obj):
            # Получаем связанные объекты DetailProductModel для текущего объекта Product
        details = obj.details.all()
            # Сериализуем каждый объект DetailProductModel
        serializer = DetailSerializer(details, many=True)
        return serializer.data


