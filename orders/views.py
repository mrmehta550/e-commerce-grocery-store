from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect
from cart.models import Cart
from .models import Order, OrderItem
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from collections import defaultdict
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse

def checkout(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.items.all()

    provider_map = defaultdict(list)

    # Group by provider
    for item in cart_items:
        provider = item.product.provider
        provider_map[provider].append(item)

    # Create orders per provider
    for provider, items in provider_map.items():

        total_price = 0

        order = Order.objects.create(
            user=request.user,
            provider=provider,

            # 🔥 Billing (get from POST)
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            address=request.POST.get('address'),
            address2=request.POST.get('address2'),
            country=request.POST.get('country'),
            zip_code=request.POST.get('zip_code'),

            payment_method=request.POST.get('payment_method'),
            status='placed'
        )

        for item in items:
            item_total = item.product.price * item.quantity
            total_price += item_total

            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # ✅ Save total
        order.total_price = total_price
        order.save()

    # Clear cart
    cart.items.all().delete()

    return redirect('order_success')
    
def success_view(request):
    return render(request, 'success.html')

def order_success(request):
    return render(request, 'providers/success.html')

def order_tracking(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)

    steps = ['placed', 'packed', 'shipped', 'delivered']

    current_index = steps.index(order.status) if order.status in steps else 0

    context = {
        'order': order,
        'steps': steps,
        'current_index': current_index
    }

    return render(request, 'tracking.html', context)

def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/my_orders.html', {'orders': orders})

def order_status_api(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)

    return JsonResponse({
        'status': order.status,
        'status_display': order.get_status_display(),
        'total_price': float(order.total_price),
    })