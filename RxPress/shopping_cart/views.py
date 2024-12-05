from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from admin_dashboard.models import Medicine
from .models import Cart, CartItem  # Import Cart and CartItem from shopping_cart.models
from orders.models import Order, OrderItem  # Import Order and OrderItem from the orders app
from django.http import JsonResponse
from datetime import datetime

def cart_view(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.cartitems.all()
        total_cost = cart.total_cost
    except Cart.DoesNotExist:
        cart_items = []
        total_cost = 0.00

    return render(request, 'shopping_cart/cart.html', {
        'cart_items': cart_items,
        'total_cost': total_cost,
    })

def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if request.method == "POST":
        new_quantity = int(request.POST.get(f'quantity_{cart_item.medicine.id}', cart_item.quantity))
        cart_item.quantity = new_quantity
        cart_item.save()
        cart_item.cart.update_total_cost()
        messages.success(request, "Cart updated successfully!")
        return redirect('shopping_cart:cart_view')

    return redirect('shopping_cart:cart_view')

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('shopping_cart:cart_view')

def add_to_cart(request):
    if request.method == "POST":
        selected_items = request.POST.getlist('selected_items')
        quantities = {key: value for key, value in request.POST.items() if key.startswith('quantity_')}
        cart, created = Cart.objects.get_or_create(user=request.user)

        for item_id in selected_items:
            try:
                medicine = Medicine.objects.get(id=item_id)
                quantity = int(quantities.get(f'quantity_{item_id}', 1))

                cart_item, created = CartItem.objects.get_or_create(
                    cart=cart,
                    medicine=medicine,
                    defaults={'quantity': quantity}
                )

                if not created:
                    cart_item.quantity += quantity
                    cart_item.save()

                messages.success(request, f"{medicine.name} added to your cart.")

            except Medicine.DoesNotExist:
                messages.error(request, f"Medicine with ID {item_id} does not exist.")
            except ValueError:
                messages.error(request, "Invalid quantity value.")

        return redirect('shopping_cart:cart_view')

    return redirect('homepage:homepage')

def place_order(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.cartitems.all()

    if not cart_items:
        messages.error(request, "Your cart is empty. Please add items to your cart before placing an order.")
        return redirect('shopping_cart:cart_view')

    total_cost = cart.total_cost
    order = Order.objects.create(user=request.user, total_cost=total_cost)

    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            medicine=cart_item.medicine,
            quantity=cart_item.quantity,
            item_cost=cart_item.total_cost
        )

    cart_items.delete()  # Clear cart after placing the order
    cart.update_total_cost()  # Ensure the cart's total is updated

    messages.success(request, f"Thank you for your order! Please prepare ₱{total_cost:.2f} upon receiving your order.")

    # Redirect to the order confirmation page with the total cost as a query parameter
    return redirect(f"{reverse('shopping_cart:order_confirmation')}?total_cost={total_cost}")

def order_confirmation(request):
    total_cost = request.GET.get('total_cost')

    if total_cost:
        total_cost = float(total_cost)  # Ensure it's a float for the template
    else:
        total_cost = 0.00

    return render(request, 'shopping_cart/order_confirmation.html', {
        'total_cost': total_cost
    })

