from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem  
from orders.models import Order, OrderItem  
from login_register.views import logout

@login_required
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

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if request.method == "POST":
        new_quantity = int(request.POST.get(f'quantity_{cart_item.medicine.id}', cart_item.quantity))
        cart_item.quantity = new_quantity
        cart_item.save()
        cart_item.cart.update_total_cost()
        return redirect('shopping_cart:cart_view')

    return redirect('shopping_cart:cart_view')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('shopping_cart:cart_view')

@login_required
def place_order(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.cartitems.all()

    if not cart_items:
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

    cart_items.delete()  
    cart.update_total_cost()  
    return redirect(f"{reverse('shopping_cart:order_confirmation')}?total_cost={total_cost}")

@login_required
def order_confirmation(request):
    total_cost = request.GET.get('total_cost')

    if total_cost:
        total_cost = float(total_cost)  # Ensure it's a float for the template
    else:
        total_cost = 0.00

    # Get the latest order for the logged-in user
    order = Order.objects.filter(user=request.user).order_by('-created_at').first()  # Assuming 'created_at' is the field that indicates when the order was created

    return render(request, 'shopping_cart/order_confirmation.html', {
        'order': order,
        'total_cost': total_cost
    })
@login_required
def logout_user(request):
    logout(request)
    messages.success(request,"You have been logged out.")
    return redirect('login_register:onboarding')
