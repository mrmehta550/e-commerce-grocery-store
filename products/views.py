from django.shortcuts import render
from django.views.generic import ListView
from .models import *
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

        if category:
            queryset = queryset.filter(category__id=category)

        if tag:
            queryset = queryset.filter(tag=tag)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    
class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'