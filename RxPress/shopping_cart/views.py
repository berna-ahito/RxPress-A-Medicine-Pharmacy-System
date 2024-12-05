from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from admin_dashboard.models import Medicine
from .models import Cart, CartItem
from .forms import CartItemForm
from django.http import JsonResponse

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
        form = CartItemForm(request.POST, instance=cart_item)

        if form.is_valid():
            form.save()
            messages.success(request, "Cart updated successfully!")
            return redirect('shopping_cart:cart_view')
        else:
            messages.error(request, "Failed to update cart. Please check the quantity.")
    
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
