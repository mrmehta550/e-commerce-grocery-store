from django.urls import path
from .views import *
from .views import ProductDetailView

urlpatterns = [
    path('', ShopView.as_view(), name='shop'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]