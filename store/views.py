import telegram
import asyncio
from rest_framework import viewsets, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend


from django.core.mail import send_mail
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.conf import settings


from .models import Product, CollectionProduct, Category, Subcategory, NavMenu
from .serializers import ProductSerializer, CollectionProductSerializer, CategorySerializer, SubcategorySerializer, NavMenuSerializer, AllDataSerializer

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


class ProductViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
    'id': ['exact'],
    'name': ['icontains'],
    'category': ['exact'],
    'subcategory': ['exact'],
    'sale': ['gt'],
    }
    def get_queryset(self):
        queryset = self.queryset
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset
    #@method_decorator(cache_page(CACHE_TTL))
    #def dispatch(self, request, *args, **kwargs):
        #return super().dispatch(request, *args, **kwargs)
    

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
        products = request.data.get('products')
        order_total = request.data.get('order_total')
        subject = f'Новая заявка от {name}'
        message = f'<html><head><style>table, th, td {{border: 1px solid black;}}</style></head><body>Получена новая заявка:<br><br>Имя: {name}<br>Номер телефона: {phone}<br>Сумма заказа: {order_total}<br><br><table><tr><th>Название товара</th><th>Цена</th><th>Количество</th></tr>'
        for product in products:
            message += f'<tr><td>{product["name"]}</td><td>{product["price"]}</td><td>{product["quantity"]}</td></tr>'
        message += '</table></body></html>'
        recipient_list = [settings.EMAIL_HOST_USER]

        if EmailSender.send_email(subject, message, recipient_list):
            return Response({'message': 'Email sent successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Email could not be sent.'}, status=status.HTTP_400_BAD_REQUEST)



async def send_telegram_message(chat_id, message_text):
    bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
    await bot.send_message(chat_id=chat_id, text=message_text,  parse_mode='HTML')


class TelegramViewSet(viewsets.ViewSet):
    def create(self, request):
        phone = request.data.get('phone')
        name = request.data.get('name')
        products = request.data.get('products')
        order_total = request.data.get('order_total')

        chat_id = '476053815'
        message_text = f'Получена новая заявка от: <b style="color: red">{name}</b> \n\n📞  Номер телефона: <b>{phone}</b>\n\n🛋️  <b>Список товаров:</b>'
        for product in products:
            message_text += f"\n🔹 <b>{product['name']}</b> - {product['quantity']} x {product['price']} ₽"
        message_text += f"\n\n💵 <b>Сумма заказа:</b> {order_total} ₽"

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(send_telegram_message(chat_id, message_text))

        return Response({'status': 'success'}, status=status.HTTP_201_CREATED)


