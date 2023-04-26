from django.urls import path, include

from rest_framework import routers

from store.views import ProductViewSet, CollectionProductViewSet, EmailViewSet, CategoryViewSet, SubcategoryViewSet, NavMenuViewSet, AllDataViewSet


router = routers.DefaultRouter()
router.register(r'product', ProductViewSet)
router.register(r'collection', CollectionProductViewSet)
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'subcategories', SubcategoryViewSet)
router.register(r'menu', NavMenuViewSet, basename='navmenu')
router.register(r'alldata', AllDataViewSet, basename='alldata')
router.register(r'send_emai', EmailViewSet, basename='send_email')


urlpatterns = [
    path('', include(router.urls))
]
