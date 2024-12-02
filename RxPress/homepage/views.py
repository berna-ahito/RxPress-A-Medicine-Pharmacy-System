from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Medicine, Cart, Order
from .forms import AddToCartForm, MedicineSearchForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from django.shortcuts import redirect
from django.contrib import messages
from .models import Medicine, Cart


# from .forms import RegisterForm

# def homepage(request):
#     medicines = Medicine.objects.all()
#     return render(request, 'homepage/homepage.html', {'medicines': medicines})

# added code

def homepage(request):
    medicines = Medicine.objects.all()
    search_form = MedicineSearchForm(request.GET or None)

    if search_form.is_valid():
        query = search_form.cleaned_data['search_query']
        if query:
            medicines = medicines.filter(name__icontains=query)

    add_to_cart_form = AddToCartForm()

    return render(request, 'homepage/homepage.html', {
        'medicines': medicines,
        'search_form': search_form,
        'add_to_cart_form': add_to_cart_form,
    })



def order_view(request):
    orders = Order.objects.all()
    return render(request, 'order.html', {'orders': orders})


# def homepage(request):
#     return render(request, 'homepage.html')

# def order_view(request):
#     return render(request, 'order.html')

def cart_view(request):
    return render(request, 'cart.html')


def update_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(Cart, id=item_id)
        cart_item.quantity = int(request.POST.get('quantity', 1))
        cart_item.save()
    return redirect('homepage:cart_view')

def remove_from_cart(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(Cart, id=item_id)
        cart_item.delete()
    return redirect('homepage:cart_view')

def checkout(request):
    # Handle checkout logic here
    return redirect('homepage:order_view')


# def add_to_cart(request):
#     if request.method == 'POST':
#         selected_items = request.POST.getlist('selected_items')
#         for item_id in selected_items:
#             quantity = request.POST.get(f'quantity_{item_id}')
#             medicine = Medicine.objects.get(id=item_id)
#             Cart.objects.create(
#                 medicine=medicine,
#                 quantity=int(quantity),
#                 user=request.user  # Assuming the user is logged in
#             )
#         return redirect('homepage:cart_view')  # Redirect to the cart page
#     return HttpResponse("Invalid Request", status=400)

# added code
# def add_to_cart(request):
#     if request.method == "POST":
#         selected_items = request.POST.getlist('selected_items')  # List of selected item IDs
#         for item_id in selected_items:
#             quantity = int(request.POST.get(f'quantity_{item_id}', 1))
#             medicine = get_object_or_404(Medicine, id=item_id)
            
#             # Check if the item already exists in the user's cart
#             cart_item, created = Cart.objects.get_or_create(
#                 user=request.user, medicine=medicine,
#                 defaults={'quantity': quantity}
#             )
#             if not created:  # If the item already exists, update the quantity
#                 cart_item.quantity += quantity
#                 cart_item.save()

#         return redirect('homepage:cart_view')  # Redirect to the cart page
#     return HttpResponse("Invalid Request", status=400)


# def add_to_cart(request):
#     if request.method == 'POST':
#         form = AddToCartForm(request.POST)
#         if form.is_valid():
#             medicine_id = form.cleaned_data['medicine_id']
#             quantity = form.cleaned_data['quantity']
#             # Add the item to the cart (custom logic for your cart model)
#             messages.success(request, "Item added to cart!")
#             return HttpResponseRedirect(reverse('homepage:homepage'))
#     return HttpResponseRedirect(reverse('homepage:homepage'))



def add_to_cart(request):
    if request.method == "POST":
        selected_items = request.POST.getlist('selected_items')  # Get all selected checkboxes
        quantities = {key: value for key, value in request.POST.items() if key.startswith('quantity_')}  # Quantities
        
        for item_id in selected_items:
            try:
                medicine = Medicine.objects.get(id=item_id)
                quantity = int(quantities.get(f'quantity_{item_id}', 1))  # Default quantity to 1 if missing
                
                # Check if the item is already in the cart
                cart_item, created = Cart.objects.get_or_create(
                    user=request.user,
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






def logout(request):
    request.session.clear()  # Clear user session data
    messages.success(request, 'You have been logged out.')
    return redirect('login.html')  # Redirect to the login page after logout