from django.shortcuts import render

from django.contrib import messages
from django.shortcuts import render, redirect
from cart.models import Cart
from .models import Order, OrderItem

def checkout_view(request):
    cart = Cart.objects.get(user=request.user)

    subtotal = sum(item.total_price() for item in cart.items.all())

    if request.method == "POST":
        # create order
        order = Order.objects.create(
            user=request.user,
            total_price=subtotal
        )

        # create order items
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # clear cart
        cart.items.all().delete()

        messages.success(request, "Order placed successfully!")  # ✅ inside POST

        return redirect('order_success')

    return render(request, 'checkout.html', {
        'cart': cart,
        'subtotal': subtotal
    })
    
def success_view(request):
    return render(request, 'success.html')