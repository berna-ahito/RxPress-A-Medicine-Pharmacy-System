from django.shortcuts import get_object_or_404, redirect, render
from admin_dashboard.models import Medicine
from django.contrib.auth.decorators import login_required
from login_register.views import logout
from django.contrib import messages
from shopping_cart.models import Cart, CartItem

@login_required
def homepage(request):
    medicines = Medicine.objects.all()  # Fetch all medicines from the database

    return render(request, 'homepage.html', {
        'medicines': medicines,
    })

@login_required
def cart_view(request):
    # Logic for cart view
    return render(request, 'homepage/cart_view.html')

@login_required
def order_view(request):
    # Logic for order view
    return render(request, 'homepage/order_view.html')

@login_required
def logout_user(request):
    logout(request)
    return redirect('login_register:login')

@login_required
def add_to_cart(request, product_id):
    medicine = get_object_or_404(Medicine, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the item already exists in the cart
    cart_item, item_created = CartItem.objects.get_or_create(cart=cart, medicine=medicine)

    if not item_created:
        # Increment the existing quantity by the value from the form
        quantity_to_add = int(request.POST.get('quantity', 1))
        cart_item.quantity += quantity_to_add
        cart_item.save()
    else:
        # Set the initial quantity for the new item
        quantity_to_add = int(request.POST.get('quantity', 1))
        cart_item.quantity = quantity_to_add
        cart_item.save()

    # Update the cart's total cost
    cart.update_total_cost()

    return redirect('shopping_cart:cart_view')

@login_required
def product_details(request, product_id):
    product = get_object_or_404(Medicine, id=product_id)
    return render(request, 'product_details.html', {
        'product': product
    })