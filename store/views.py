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
    'category': ['exact'],
    'subcategory': ['exact'],
    'sale': ['gt'],
    }
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
    http_method_names = ['get']
    queryset = NavMenu.objects.all()
    serializer_class = NavMenuSerializer

class AllDataViewSet(viewsets.ReadOnlyModelViewSet):
    http_method_names = ['get']
    serializer_class = AllDataSerializer
    queryset = Category.objects.all()


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


async def send_telegram_message(chat_id, message_text):
    bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)
    await bot.send_message(chat_id=chat_id, text=message_text)

class TelegramViewSet(viewsets.ViewSet):
    def create(self, request):
        phone = request.data.get('phone')
        name = request.data.get('name')
        products = request.data.get('products')
        order_total = request.data.get('order_total')

        chat_id = '476053815'
        message_text = f"Получена новая заявка от: {name} ({phone})\n {products}\n {order_total}"
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(send_telegram_message(chat_id, message_text))

        return Response({'status': 'success'}, status=status.HTTP_201_CREATED)
