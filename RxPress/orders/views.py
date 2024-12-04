from django.shortcuts import render, redirect
from .models import Order
from shopping_cart.models import CartItem
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)  # Fetch cart items for the logged-in user
    
    if not cart_items:
        messages.error(request, "Your cart is empty.")
        return redirect('shopping_cart:cart_view')
    
    # Calculate total cost for the order
    total_cost = cart_items.aggregate(total=Sum('total_cost'))['total'] or 0
    
    # Create order and associate it with the cart items
    order = Order.objects.create(user=request.user, total_cost=total_cost)
    
    # Create order items
    for cart_item in cart_items:
        order.items.create(medicine=cart_item.medicine, quantity=cart_item.quantity, item_cost=cart_item.total_cost)

    # Clear cart items after checkout
    cart_items.delete()
    
    messages.success(request, "Your order has been placed successfully.")
    return redirect('orders:order_view')

@login_required
def order_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')  # Fetch orders for the logged-in user
    return render(request, 'orders/orders.html', {'orders': orders})