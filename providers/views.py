from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product, Category
from .models import Provider
from orders.models import Order
from orders.utils import send_order_status_email

def _is_provider_user(user):
    profile = getattr(user, 'profile', None)
    if profile is not None:
        return getattr(profile, 'role', None) == 'provider'

    return hasattr(user, 'provider')


@login_required
def provider_dashboard(request):
    if not _is_provider_user(request.user):
        return redirect('home')

    provider = getattr(request.user, 'provider', None)
    if provider is None:
        return redirect('home')

    products = Product.objects.filter(provider=provider)
    orders = Order.objects.filter(provider=provider).order_by('-created_at')[:5]

    context = {
        'provider': provider,
        'products': products,
        'orders': orders,
        'total_products': products.count(),
        'total_orders': Order.objects.filter(provider=provider).count(),
    }

    return render(request, 'providers/dashboard.html', context)


@login_required
def provider_orders(request):
    if not _is_provider_user(request.user):
        return redirect('home')

    provider = getattr(request.user, 'provider', None)
    if provider is None:
        return redirect('home')

    orders = Order.objects.filter(provider=provider).order_by('-created_at')

    return render(request, 'providers/orders.html', {
        'orders': orders
    })


@login_required
def add_product(request):
    if not _is_provider_user(request.user):
        return redirect('home')

    provider = getattr(request.user, 'provider', None)
    if provider is None:
        return redirect('home')

    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')

        if not name or not price or not description or not category_id or not image:
            messages.error(request, 'Please complete all fields and upload an image.')
            return render(request, 'providers/add_product.html', {'categories': categories})

        category = get_object_or_404(Category, id=category_id)

        Product.objects.create(
            provider=provider,
            name=name,
            price=price,
            description=description,
            category=category,
            image=image,
        )

        messages.success(request, 'Product created successfully.')
        return redirect('provider_dashboard')

    return render(request, 'providers/add_product.html', {'categories': categories})


@login_required
def delete_product(request, pk):
    if not _is_provider_user(request.user):
        return redirect('home')

    provider = getattr(request.user, 'provider', None)
    if provider is None:
        return redirect('home')

    product = get_object_or_404(Product, pk=pk, provider=provider)
    product.delete()
    return redirect('provider_dashboard')


@login_required
def update_order_status(request, pk, status):
    if not _is_provider_user(request.user):
        return redirect('home')

    provider = getattr(request.user, 'provider', None)
    if provider is None:
        return redirect('home')

    order = get_object_or_404(Order, pk=pk, provider=provider)

    valid_status = ['packed', 'shipped', 'delivered']

    if status in valid_status:
        order.status = status
        order.save()

        if status in ['shipped', 'delivered']:
            send_order_status_email(order, request)

    return redirect('provider_orders')