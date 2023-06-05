from django.urls import path, include

from rest_framework import routers
from django.conf import settings
from django.conf.urls.static  import static

from store.views import ProductViewSet, CollectionProductViewSet, EmailViewSet, TelegramViewSet , CategoryViewSet, SubcategoryViewSet, NavMenuViewSet, AllDataViewSet, DetailProductModelViewSet, ColorViewSet, MaterialViewSet, StyleViewSet
 

router = routers.DefaultRouter()
router.register(r'product', ProductViewSet)
router.register(r'colors', ColorViewSet, basename='color')
router.register(r'materials', MaterialViewSet, basename='material')
router.register(r'style', StyleViewSet, basename='style')
router.register(r'product_detail', DetailProductModelViewSet, basename='product_detail')
router.register(r'collection', CollectionProductViewSet)
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'subcategories', SubcategoryViewSet)
router.register(r'menu', NavMenuViewSet, basename='navmenu')
router.register(r'alldata', AllDataViewSet, basename='alldata')
router.register(r'send_email', EmailViewSet, basename='send_email')
router.register(r'send_telegram', TelegramViewSet, basename='send_telegram')


urlpatterns = [
    path('', include(router.urls))
] 
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)