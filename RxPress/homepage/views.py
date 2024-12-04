from django.shortcuts import redirect, render
from django.contrib.auth import logout
from admin_dashboard.models import Medicine
from orders.models import Order
from shopping_cart.models import Cart
from .forms import AddToCartForm, MedicineSearchForm

def homepage(request):
    medicines = Medicine.objects.all()  # Fetch all medicines from the database
    search_form = MedicineSearchForm(request.GET or None)  # Search form

    if search_form.is_valid():
        query = search_form.cleaned_data['search_query']
        if query:
            medicines = medicines.filter(name__icontains=query)  # Filter based on search query

    add_to_cart_form = AddToCartForm()

    return render(request, 'homepage/homepage.html', {
        'medicines': medicines,
        'search_form': search_form,
        'add_to_cart_form': add_to_cart_form,
    })

def cart_view(request):
    # Logic for cart view
    return render(request, 'homepage/cart_view.html')

def order_view(request):
    # Logic for order view
    return render(request, 'homepage/order_view.html')

def logout_view(request):
    logout(request)
    return redirect('homepage:homepage')
