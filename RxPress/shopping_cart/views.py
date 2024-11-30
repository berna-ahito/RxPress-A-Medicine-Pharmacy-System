from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, CartItem
from django.conf import settings

def cart_detail(request):
    from orders.models import Order  # Import inside the function to avoid circular import
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    return render(request, 'shopping_cart/cart_detail.html', {'cart': cart, 'cart_items': cart_items})

def add_to_cart(request):
    # Logic to add an item to the cart
    # You can modify this logic as per your requirements
    return redirect('shopping_cart:cart_detail')

def update_cart(request):
    # Logic to update the cart
    # You can modify this logic as per your requirements
    return redirect('shopping_cart:cart_detail')

def remove_from_cart(request):
    # Logic to remove an item from the cart
    # You can modify this logic as per your requirements
    return redirect('shopping_cart:cart_detail')

def place_order(request):
    # Logic to place an order
    # You can modify this logic as per your requirements
    return redirect('shopping_cart:cart_detail')
