from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from products.models import Product
from collections import defaultdict
from django.shortcuts import redirect
from cart.models import Cart
from orders.models import Order
from cart.models import CartItem

# ✅ ADD TO CART
@login_required(login_url='login')
def add_to_cart(request, pk):
    product = get_object_or_404(Product, id=pk)

    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


# ✅ CART VIEW
@login_required(login_url='login')
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)

    subtotal = sum(item.total_price() for item in cart.items.all())

    return render(request, 'cart.html', {
        'cart': cart,
        'subtotal': subtotal
    })


# ✅ UPDATE QUANTITY
@login_required(login_url='login')
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)

    if request.method == "POST":
        quantity = int(request.POST.get('quantity'))
        item.quantity = quantity
        item.save()

    return redirect('cart')


# ✅ REMOVE ITEM
@login_required(login_url='login')
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart')

def checkout(request):
    cart = Cart.objects.get(user=request.user)
    cart_items = cart.items.all()

    # 🧠 Step 1: Group by provider
    provider_map = defaultdict(list)

    for item in cart_items:
        provider = item.product.provider
        provider_map[provider].append(item)
        
    for provider, items in provider_map.items():

        order = Order.objects.create(
            user=request.user,
            provider=provider,
            status="Pending"
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

    # 🧹 Step 3: Clear cart
    cart.items.all().delete()

    return redirect('order_success')