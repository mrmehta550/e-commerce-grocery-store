from django.urls import path
from .views import register_view, login_view, logout_view,MyAccountView
from .api_views import RegisterAPIView, LoginAPIView

urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('api/register/', RegisterAPIView.as_view(), name='api_register'),
    path('api/login/', LoginAPIView.as_view(), name='api_login'),
    path('my-account/', MyAccountView.as_view(), name='my_account'),
]