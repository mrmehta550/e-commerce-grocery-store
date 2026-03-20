from django.urls import path
from . import views

urlpatterns = [
    path('index.html',views.HomeView.as_view(), name='home'),
    path('about.html',views.AboutView.as_view(), name='about'),
    path('cart.html',views.CartView.as_view(), name='cart'),
    path('checkout.html',views.CheckoutView.as_view(), name='checkout'),
    path('contact-us.html',views.ContactView.as_view(), name='contact-us'),
    path('gallery.html',views.GalleryView.as_view(), name='gallery'),
    path('my-account.html',views.AccountView.as_view(), name='my-account'),
    path('shop-detail.html',views.ShopDetail.as_view(), name='shop-detail'),
    path('shop.html',views.ShopView.as_view(), name='shop'),
    path('wishlist.html',views.WishlistView.as_view(), name='wishlist'),
] 
