from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('success/', views.success_view, name='order_success'),
    # path('track-order/<int:order_id>/', OrderTrackingView.as_view(), name='order_tracking'),
    path('tracking/<int:pk>/', views.order_tracking, name='order_tracking'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('status/<int:pk>/', views.order_status_api, name='order_status_api'),

]