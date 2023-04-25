from django.urls import path, include

from rest_framework import routers

from store.views import ProductViewSet, CollectionProductViewSet, EmailViewSet, CategoryViewSet, SubcategoryViewSet


router = routers.DefaultRouter()
router.register(r'product', ProductViewSet)
router.register(r'collection', CollectionProductViewSet)
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'subcategories', SubcategoryViewSet)
router.register(r'send_emai', EmailViewSet, basename='send_email')


urlpatterns = [
    path('', include(router.urls))
]
