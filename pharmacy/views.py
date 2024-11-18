from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import Medicine, Order, ShoppingCart, CartItem

# Utility to get or create a cart
def get_cart(user):
    cart, created = ShoppingCart.objects.get_or_create(user=user)
    return cart

# Homepage View
def homepage(request):
    medicines = Medicine.objects.all()
    return render(request, 'pharmacy/homepage.html', {'medicines': medicines})

# Cart View
@login_required
def cart_view(request):
    cart = get_cart(request.user)
    cart_items = cart.items.all()
    total_cost = cart.total_cost

    context = {
        'cartItemsResult': cart_items,
        'totalCostResult': total_cost
    }
    return render(request, 'pharmacy/cart.html', context)

# Add to Cart
@login_required
def add_to_cart(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selected_items')
        for item in selected_items:
            medicine = get_object_or_404(Medicine, id=item)
            quantity = int(request.POST.get(f'quantity_{medicine.id}', 1))
            
            cart = get_cart(request.user)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                medicine=medicine,
                defaults={'quantity': quantity}
            )
            if not created:
                cart_item.quantity += quantity
                cart_item.save()

        messages.success(request, "Items added to cart successfully.")
        return redirect('pharmacy:cart_view')

@login_required
def update_cart(request):
    if request.method == 'POST':
        cart = get_cart(request.user)  # Retrieve the user's cart
        updated = False

        # Loop through each cart item and update its quantity
        for cart_item in cart.items.all():
            quantity_key = f'quantity_{cart_item.medicine.id}'  # Get the updated quantity
            new_quantity = request.POST.get(quantity_key)

            if new_quantity:
                new_quantity = int(new_quantity)
                if new_quantity != cart_item.quantity:
                    cart_item.quantity = new_quantity  # Update the quantity
                    cart_item.save()  # Save the updated CartItem
                    updated = True

        if updated:
            cart.update_total_cost()  # Recalculate the total cost of the cart
            messages.success(request, "Cart updated successfully.")
        else:
            messages.info(request, "No changes were made to the cart.")

        return redirect('pharmacy:cart_view')  # Redirect to the cart view

    return redirect('pharmacy:cart_view')  # Redirect if not a POST request

@login_required
def remove_from_cart(request):
    if request.method == 'POST' and request.is_ajax():
        medicine_id = request.POST.get('medicine_id')
        medicine = get_object_or_404(Medicine, id=medicine_id)

        # Find and delete the cart item associated with this medicine
        cart = get_cart(request.user)
        cart_item = CartItem.objects.filter(medicine=medicine, cart=cart).first()

        if cart_item:
            cart_item.delete()  # Delete the cart item
            cart.update_total_cost()  # Recalculate the total cost after deletion
            return JsonResponse({
                'success': True,
                'total_cost': f'{cart.total_cost:.2f}',
                'message': f'{medicine.name} has been removed from your cart.'
            })
        else:
            return JsonResponse({'success': False, 'message': 'Item not found in cart.'})

    return JsonResponse({'success': False, 'message': 'Invalid request.'})

# Place Order
@login_required
def place_order(request):
    if request.method == 'POST':
        cart = get_cart(request.user)
        cart_items = cart.items.all()
        total_amount = sum(item.total_cost for item in cart_items)

        for item in cart_items:
            # Check if there's enough stock available
            if item.medicine.quantity >= item.quantity:
                # Create order and reduce quantity in stock
                Order.objects.create(
                    medicine=item.medicine,
                    user=request.user,
                    quantity=item.quantity,
                    total_cost=item.total_cost,
                    is_cart=False  # Set is_cart to False since it's now an order
                )
                # Update the medicine quantity in stock
                item.medicine.quantity -= item.quantity
                item.medicine.save()  # Save the updated quantity to the database

                # Remove the item from the cart
                item.delete()
            else:
                # Handle case where there is not enough stock
                messages.error(request, f"Not enough stock for {item.medicine.name}.")

        # Recalculate the total cost of the cart
        cart.update_total_cost()

        # Notify user and redirect to homepage
        messages.success(
            request,
            f"Order placed successfully. Please prepare ₱{total_amount:.2f} upon delivery."
        )
        return redirect('pharmacy:homepage')

# User Registration
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('pharmacy:homepage')
    else:
        form = RegisterForm()

    return render(request, 'pharmacy/register.html', {'form': form})

@login_required
def account_view(request):
    return render(request, 'pharmacy/account.html', {'user': request.user})

@login_required
def edit_account(request):
    user = request.user

    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_first_name = request.POST.get('first_name')
        new_password = request.POST.get('password')
        new_password_confirmation = request.POST.get('password_confirmation')
        delete_account = request.POST.get('delete_account')

        if delete_account == 'True':
            # Handle account deletion
            user.delete()
            messages.success(request, "Your account has been deleted.")
            return redirect('pharmacy:homepage')  # Redirect to homepage after account deletion

        if new_username:
            user.username = new_username
        if new_first_name:
            user.first_name = new_first_name
        if new_password and new_password == new_password_confirmation:
            user.set_password(new_password)
            update_session_auth_hash(request, user)  # Keep the user logged in after password change

        # Save the updated user information
        user.save()

        messages.success(request, "Your account details have been updated successfully.")
        return redirect('pharmacy:account')  # Redirect to account page after successful update

    return render(request, 'pharmacy/edit_account.html', {'user': user})  # Render the edit account page on GET request

@login_required
def place_order(request):
    if request.method == 'POST':
        cart = get_cart(request.user)
        cart_items = cart.items.all()
        total_amount = sum(item.total_cost for item in cart_items)

        for item in cart_items:
            # Check if there's enough stock available
            if item.medicine.quantity >= item.quantity:
                # Create order and reduce quantity in stock
                Order.objects.create(
                    medicine=item.medicine,
                    user=request.user,
                    quantity=item.quantity,
                    total_cost=item.total_cost,
                    is_cart=False  # Set is_cart to False since it's now an order
                )
                # Update the medicine quantity in stock
                item.medicine.quantity -= item.quantity
                item.medicine.save()  # Save the updated quantity to the database

                # Remove the item from the cart
                item.delete()
            else:
                # Handle case where there is not enough stock
                messages.error(request, f"Not enough stock for {item.medicine.name}.")

        # Recalculate the total cost of the cart
        cart.update_total_cost()

        # Notify user and redirect to homepage
        messages.success(
            request,
            f"Order placed successfully. Please prepare ₱{total_amount:.2f} upon delivery."
        )
        return redirect('pharmacy:homepage')
    
@login_required
def update_cart(request):
    if request.method == 'POST':
        # Update cart logic
        cart = ShoppingCart.objects.get(user=request.user)
        # Update cart items, quantities, etc.
        for item in cart.items.all():
            quantity = request.POST.get(f'quantity_{item.id}')
            if quantity:
                item.quantity = int(quantity)
                item.save()
        cart.update_total_cost()  # Recalculate the total cost

        return redirect('pharmacy:cart_view')  # Redirect to the cart view

    return redirect('pharmacy:cart_view')  # Redirect if not a POST request
