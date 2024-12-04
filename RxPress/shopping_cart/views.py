from django.shortcuts import render, get_object_or_404, redirect
from .models import Cart, CartItem
from admin_dashboard.models import Medicine
from django.contrib import messages

def cart_view(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)  # Fetch cart items for the logged-in user
    return render(request, 'cart.html', {'cart_items': cart_items})

def update_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.quantity = int(request.POST.get('quantity', 1))
        cart_item.save()
    return redirect('shopping_cart:cart_view')

def remove_from_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id)
        cart_item.delete()
    return redirect('shopping_cart:cart_view')

def add_to_cart(request):
    if request.method == "POST":
        selected_items = request.POST.getlist('selected_items')  # Get all selected checkboxes
        quantities = {key: value for key, value in request.POST.items() if key.startswith('quantity_')}  # Quantities
        
        for item_id in selected_items:
            try:
                medicine = Medicine.objects.get(id=item_id)
                quantity = int(quantities.get(f'quantity_{item_id}', 1))  # Default quantity to 1 if missing
                
                # Check if the item is already in the cart
                cart_item, created = CartItem.objects.get_or_create(
                    cart__user=request.user,
                    medicine=medicine,
                    defaults={'quantity': quantity}
                )
                
                if not created:  # If the item already exists, update the quantity
                    cart_item.quantity += quantity
                    cart_item.save()
                
                messages.success(request, f"{medicine.name} added to your cart.")
            
            except Medicine.DoesNotExist:
                messages.error(request, f"Medicine with ID {item_id} does not exist.")
            except ValueError:
                messages.error(request, "Invalid quantity value.")
        
        return redirect('homepage:homepage')  # Redirect back to the homepage
    
    return redirect('homepage:homepage')
