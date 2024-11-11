from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, update_session_auth_hash
from django.contrib import messages
from .forms import RegisterForm, EditProfileForm
from django.db.models import Sum, F
from .models import Medicine, Order, Profile

# Homepage View
def homepage(request):
    medicines = Medicine.objects.all()
    return render(request, 'pharmacy/homepage.html', {'medicines': medicines})

# Cart View: Adjust for total cost calculation
def cart_view(request):
    cart_items = Order.objects.filter(is_cart=True, user=request.user)
    total_cost = sum(item.total_cost for item in cart_items)

    context = {
        'cartItemsResult': cart_items,
        'totalCostResult': total_cost
    }
    return render(request, 'pharmacy/cart.html', context)

# Add to Cart: Store items in the cart with quantities
def add_to_cart(request):
    if request.method == 'POST':
        selected_items = request.POST.getlist('selected_items')
        
        for item in selected_items:
            medicine_id = item
            quantity = int(request.POST.get(f'quantity_{medicine_id}', 1))
            medicine = get_object_or_404(Medicine, id=medicine_id)

            order_item, created = Order.objects.get_or_create(
                medicine=medicine,
                user=request.user,  # Add user reference
                is_cart=True,
                defaults={'quantity': quantity}
            )

            if not created:
                order_item.quantity += quantity
                order_item.save()

        return redirect('pharmacy:cart_view')

# Update Cart: Update quantity of cart items
def update_cart(request):
    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('quantity_'):
                medicine_id = key.split('_')[1]
                quantity = int(value)
                order_item = get_object_or_404(Order, medicine_id=medicine_id, is_cart=True, user=request.user)
                order_item.quantity = quantity
                order_item.save()

        return redirect('pharmacy:cart_view')

# Place Order: Convert cart items to orders
def place_order(request):
    if request.method == 'POST':
        cart_items = Order.objects.filter(is_cart=True, user=request.user)
        total_amount = sum(item.total_cost for item in cart_items)

        # Move items from cart to orders
        cart_items.update(is_cart=False)

        # You may create a new Order record here if needed
        messages.success(request, f"Thank you for your order! Your purchase has been successfully completed. Please prepare ₱{total_amount:.2f} upon receiving your order.")
        return redirect('pharmacy:cart_view')


# Remove from Cart
def remove_from_cart(request):
    if request.method == 'POST':
        medicine_id = request.POST.get('medicine_id')
        order_item = get_object_or_404(Order, medicine_id=medicine_id, is_cart=True)
        order_item.delete()
        return redirect('pharmacy:cart_view')

# User Registration View
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful! Welcome!")
            return redirect('pharmacy:homepage')  # Ensure that 'pharmacy:homepage' is defined in your urls.py
    else:
        form = RegisterForm()

    return render(request, 'pharmacy/register.html', {'form': form})

# Account View
def account_view(request):
    return render(request, 'pharmacy/account.html')

# Edit Account View
def edit_account(request):
    if request.method == 'POST':
        user = request.user
        new_first_name = request.POST.get('first_name')
        new_username = request.POST.get('username')
        new_password = request.POST.get('password')
        new_password_confirmation = request.POST.get('password_confirmation')
        new_email = request.POST.get('email')
        new_gender = request.POST.get('gender')

        # Update user information
        user.first_name = new_first_name
        user.username = new_username
        user.email = new_email
        
        if new_password:
            if new_password == new_password_confirmation:
                user.set_password(new_password)
                update_session_auth_hash(request, user)  # Keep user logged in after password change
            else:
                messages.error(request, "Passwords do not match!")
                return render(request, 'pharmacy/edit_account.html')

        # Ensure Profile exists for user
        profile, created = Profile.objects.get_or_create(user=user)

        # Update Profile (gender)
        profile.gender = new_gender  # Access the profile related to the user
        profile.save()

        user.save()

        # Redirect to the account page after successful update
        messages.success(request, "Profile updated successfully.")
        return redirect('pharmacy:account')

    return render(request, 'pharmacy/edit_account.html')
