from django.db import models
from providers.models import Provider


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    button_text = models.CharField(max_length=100, default="Shop Now")

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY_CHOICES = [
        ('top', 'Top Featured'),
        ('best', 'Best Seller'),
        ('normal', 'Normal'),
    ]
    provider = models.ForeignKey(Provider, on_delete=models.CASCADE, null=True,related_name='products')
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')

    tag = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='normal')
    is_sale = models.BooleanField(default=False)
    is_new = models.BooleanField(default=False)

    def __str__(self):
        return self.name