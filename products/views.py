from django.shortcuts import render
from django.db.models import Q
from django.views.generic import ListView
from .models import *
from django.views.generic import DetailView
from django.shortcuts import render, get_object_or_404
from products.models import Product
from django.views.generic import DetailView

class ShopView(ListView):
    model = Product
    template_name = 'shop.html'
    context_object_name = 'products'
    paginate_by = 8

    def get_queryset(self):
        queryset = Product.objects.all()

        category = self.request.GET.get('category')
        tag = self.request.GET.get('tag')
        query = self.request.GET.get('q')

        if category:
            queryset = queryset.filter(category__id=category)

        if tag:
            queryset = queryset.filter(tag=tag)

        if query:
            queryset = queryset.filter(
                models.Q(name__icontains=query) |
                models.Q(description__icontains=query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    
class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop-detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product = self.get_object()

        # Related products
        context['related_products'] = Product.objects.filter(
            category=product.category
        ).exclude(id=product.id)[:8]

        return context