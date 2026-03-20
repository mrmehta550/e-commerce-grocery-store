from django.urls import path
from .views import *

urlpatterns = [
    path('checkout/', checkout_view, name='checkout'),
    path('success/', success_view, name='order_success')
]