from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from products.models import Product


# ✅ ADD TO CART
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
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)

    subtotal = sum(item.total_price() for item in cart.items.all())

    return render(request, 'cart.html', {
        'cart': cart,
        'subtotal': subtotal
    })


# ✅ UPDATE QUANTITY
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)

    if request.method == "POST":
        quantity = int(request.POST.get('quantity'))
        item.quantity = quantity
        item.save()

    return redirect('cart')


# ✅ REMOVE ITEM
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart')