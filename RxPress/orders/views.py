from django.shortcuts import render, redirect
from .models import Order, OrderItem
from shopping_cart.models import CartItem
from django.contrib import messages
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from login_register.views import logout

@login_required
def checkout(request):
    # Get cart items for the current user
    cart_items = CartItem.objects.filter(cart__user=request.user)

    # Check if the cart is empty
    if not cart_items:
        return redirect('shopping_cart:cart_view')

    # Calculate the total cost of the cart items
    total_cost = cart_items.aggregate(total=Sum('total_cost'))['total'] or 0

    # Create an Order object
    order = Order.objects.create(user=request.user, total_cost=total_cost)

    # Create OrderItems for each cart item, linking them to the order
    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            medicine=cart_item.medicine,
            quantity=cart_item.quantity,
            item_cost=cart_item.total_cost
        )

    # Delete cart items after the order is placed
    cart_items.delete()

    # Success message and redirect to the order list
    return redirect('orders:order_view')

@login_required
def order_view(request):
    # Check if the user is an admin (superuser)
    if request.user.is_superuser:
        # Get all orders for all customers, ordered by creation date (newest first)
        orders = Order.objects.all().order_by('-created_at')
    else:
        # Get orders only for the current user if not an admin
        orders = Order.objects.filter(user=request.user).order_by('-created_at')

    # Pass the orders to the template
    return render(request, 'orders/orders.html', {'orders': orders})

@login_required
def logout_user(request):
    logout(request)
    return redirect('login_register:onboarding')