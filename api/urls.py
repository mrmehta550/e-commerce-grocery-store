from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register('navbar', NavbarCategoryViewSet)
router.register('business-hours', BusinessHourViewSet)
router.register('social', SocialMediaViewSet)

router.register('categories', CategoryViewSet, basename='category')
router.register('categories-products', CategoryWithProductsViewSet, basename='category-products')

router.register('products', ProductViewSet, basename='product')

router.register('cart', CartViewSet, basename='cart')
router.register('cart-items', CartItemViewSet, basename='cart-item')

router.register('orders', OrderViewSet, basename='order')

urlpatterns = router.urls