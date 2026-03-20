from django.db import models

from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # 🔥 Billing Info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

    address = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True, null=True)

    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)

    # 🔥 Payment
    payment_method = models.CharField(max_length=50)

    # 🔥 Pricing
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    # 🔥 Status
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.user.username}"
    
class OrderItem(models.Model):

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')

    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField()

    price = models.DecimalField(max_digits=10, decimal_places=2)

    def total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"