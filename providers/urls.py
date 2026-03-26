from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.provider_dashboard, name='provider_dashboard'),
    path('add-product/', views.add_product, name='add_product'),
    path('delete-product/<int:pk>/', views.delete_product, name='delete_product'),
    path('orders/', views.provider_orders, name='provider_orders'),
    path('order/<int:pk>/status/<str:status>/', views.update_order_status, name='update_order_status'),
]