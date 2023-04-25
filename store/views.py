from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings

from .models import Product, CollectionProduct, Category, Subcategory
from .serializers import ProductSerializer, CollectionProductSerializer, CategorySerializer, SubcategorySerializer 
from django_filters.rest_framework import DjangoFilterBackend


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'subcategory']


class CollectionProductViewSet(viewsets.ModelViewSet):
    queryset = CollectionProduct.objects.all()
    serializer_class = CollectionProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer


class EmailViewSet(viewsets.ViewSet):

    def create(self, request):
        phone = request.data.get('phone')
        name = request.data.get('name')
        products = request.data.get('products')
        order_total = request.data.get('order_total')
        subject = 'Новая заявка от ' + name
        message = 'Получена новая заявка:\n\nИмя: {}\nНомер телефона: {}\nСумма заказа:{}\n\nProducts:\n'.format(name, phone, order_total)
        for product in products:
            message += '  - {}: {} x {}\n'.format(product['name'], product['price'], product['quantity'])
        recipient_list = [settings.EMAIL_HOST_USER]
        sender = settings.EMAIL_HOST_USER

        if subject and message and recipient_list:
            try:
                send_mail(subject, message, sender, recipient_list)
                return Response({'message': 'Email sent successfully.'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'message': 'Email could not be sent. Error: {}'.format(str(e))}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Please provide all required fields.'}, status=status.HTTP_400_BAD_REQUEST)


