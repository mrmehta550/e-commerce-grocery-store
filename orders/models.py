
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from products.models import Product
from providers.models import Provider

User = settings.AUTH_USER_MODEL


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('placed', 'Order Placed'),
        ('packed', 'Packed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    provider = models.ForeignKey(
        Provider,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='orders'
    )

    # 🔥 Billing Info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

    address = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)

    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)

    # 🔥 Payment
    payment_method = models.CharField(max_length=50)

    # 🔥 Pricing
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # 🔥 Status (FIXED ✅)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Order {self.id} - {self.user}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return self.product.name
