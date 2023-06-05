import telegram
import asyncio
from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings


from .models import Product, CollectionProduct, Category, Subcategory, NavMenu, DetailProductModel
from .serializers import ProductSerializer ,CollectionProductSerializer, CategorySerializer, SubcategorySerializer, NavMenuSerializer, AllDataSerializer, DetailSerializer

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

from rest_framework.response import Response

class ColorViewSet(viewsets.ViewSet):
    def list(self, request):
        colors = Product.objects.values_list('color', flat=True).distinct()
        return Response(list(colors))

class MaterialViewSet(viewsets.ViewSet):
    def list(self, request):
        materials = Product.objects.values_list('material', flat=True).distinct()
        return Response(list(materials))

class StyleViewSet(viewsets.ViewSet):
    def list(self, request):
        style = Product.objects.values_list('style', flat=True).distinct()
        return Response(list(style))
    
class DetailProductModelViewSet(viewsets.ModelViewSet):
    pagination_class = None
    queryset = DetailProductModel.objects.all()
    serializer_class = DetailSerializer

class ProductViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ['date']
    filterset_fields = {
        'id': ['exact'],
        'name': ['icontains'],
        'category': ['exact'],
        'subcategory': ['exact'],
        'sale': ['gt'],
        'collection': ['exact'],
        'material': ['exact'],
        'color': ['exact'],
        'style': ['exact'],
    }
    
    def get_queryset(self):
        queryset = self.queryset
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
        
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price and max_price:
            queryset = queryset.filter(price__range=(min_price, max_price)).order_by('-price')
        elif max_price and min_price:
            queryset = queryset.filter(price__range=(max_price, min_price)).order_by('price')
        elif min_price:
            queryset = queryset.filter(price__gte=min_price).order_by('-price')
        elif max_price:
            queryset = queryset.filter(price__lte=max_price).order_by('price')
        
        quantity = self.request.query_params.get('quantity')
        if quantity:
            if quantity == '0':
                queryset = queryset.filter(quantity=0)
            elif quantity == '1':
                queryset = queryset.filter(quantity__gt=0)

        return queryset


class CollectionProductViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = CollectionProduct.objects.all()
    serializer_class = CollectionProductSerializer
   

class CategoryViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class SubcategoryViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer


class NavMenuViewSet(viewsets.ModelViewSet):
    pagination_class = None
    http_method_names = ['get']
    queryset = NavMenu.objects.all()
    serializer_class = NavMenuSerializer


class AllDataViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    serializer_class = AllDataSerializer
    queryset = Category.objects.all()


class EmailSender:
    @staticmethod
    def send_email(subject, message, recipient_list):
        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list, html_message=message)
            return True
        except Exception as e:
            print(f'Error sending email: {str(e)}')
            return False

class EmailViewSet(viewsets.ViewSet):
    def create(self, request):
        phone = request.data.get('phone')
        name = request.data.get('name')
        networks = request.data.get('networks')
        products = request.data.get('products')
        order_total = request.data.get('order_total')

        subject = f'Новая заявка от {name}'
        message = f'<html><head><style>table, th, td {{border: 1px solid black;}}</style></head><body>Получена новая заявка:<br><br>Имя: {name}<br>Номер телефона: {phone}<br>Предпочитаемый способ связи: {networks}<br>Сумма заказа: {order_total}<br>'

        message += '<br><table><tr><th>Название товара</th><th>Цена</th><th>Количество</th><th>Скидка</th><th>Рассрочка</th></tr>'

        for product in products:
            product_name = product["name"]
            product_price = product["price"]
            product_quantity = product["quantity"]
            product_sale = product.get("sale")
            product_installment = product.get("installment")

            message += f'<tr><td>{product_name}</td><td>{product_price}</td><td>{product_quantity}</td><td>{product_sale}</td><td>{"Да" if product_installment else "Нет"}</td></tr>'

        message += '</table></body></html>'
        recipient_list = [settings.EMAIL_HOST_USER]

        if EmailSender.send_email(subject, message, recipient_list):
            return Response({'message': 'Email sent successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Email could not be sent.'}, status=status.HTTP_400_BAD_REQUEST)



async def send_telegram_message(chat_id, message_text):
    bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
    await bot.send_message(chat_id=chat_id, text=message_text, parse_mode='HTML')


class TelegramViewSet(viewsets.ViewSet):
    def create(self, request):
        phone = request.data.get('phone')
        name = request.data.get('name')
        networks = request.data.get('networks')
        products = request.data.get('products')
        order_total = request.data.get('order_total')
       

        chat_id = '-1001956284492'
        message_text = f'Получена новая заявка от: <b style="color: red">{name}</b> \n\n📞  Номер телефона: <b>{phone}</b>\n\n📨  Предпочитаемый способ связи: {networks}\n\n🛋️  <b>Список товаров:</b>'
        for product in products:
            product_name = product['name']
            product_price = product['price']
            product_quantity = product['quantity']
            product_sale = product.get('sale')
            product_installment = product.get('installment')

            message_text += f"\n🔹 {product_name}\n      <b>Количество:</b> {product_quantity}\n      <b>Цена:</b> {product_price} ₽"

            if product_sale:
                message_text += f" (Скидка: {product_sale}%)"
            if product_installment:
                message_text += "\n✅ <b>Рассрочка:</b> в рассрочку"
            else:
                message_text += "\n❌ <b>Рассрочка:</b> не в рассрочку \n"
        message_text += f"\n\n💵 <b>Сумма заказа:</b> {order_total} ₽"

        

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(send_telegram_message(chat_id, message_text))

        return Response({'status': 'success'}, status=status.HTTP_201_CREATED)

