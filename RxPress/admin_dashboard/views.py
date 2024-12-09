import json
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Medicine
from .forms import MedicineForm
from login_register.views import logout
from django.shortcuts import render
from orders.models import Order
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required
def medicine_list(request):
    if not request.user.is_superuser:
        return redirect('login')  # Redirect non-admins to the login page
    
    medicines = Medicine.objects.all()  # Fetch all medicines from the database
    return render(request, 'admin_dashboard/medicine_list.html', {'medicines': medicines})

@login_required
def add_medicine(request):
    if not request.user.is_superuser:
        return redirect('login')

    if request.method == 'POST':
        form = MedicineForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_dashboard:medicine_list')  # Redirect to the URL pattern name
    else:
        form = MedicineForm()

    return render(request, 'admin_dashboard/add_medicine.html', {'form': form})

@login_required
def update_medicine(request, pk):
    if not request.user.is_superuser:
        return JsonResponse({'error': 'Unauthorized'}, status=403)

    medicine = get_object_or_404(Medicine, pk=pk)

    if request.method == 'POST':
        if request.content_type == 'application/json':
            # Handle JSON data
            try:
                data = json.loads(request.body)
                for field, value in data.items():
                    if hasattr(medicine, field):  # Ensure field exists
                        setattr(medicine, field, value)
                medicine.save()
                return JsonResponse({'message': 'Medicine updated successfully'})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)
        else:
            # Handle form data (for standard form submission)
            form = MedicineForm(request.POST, request.FILES, instance=medicine)
            if form.is_valid():
                form.save()
                return redirect('admin_dashboard:medicine_list')
            else:
                return JsonResponse({'error': 'Invalid form submission'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@login_required
def delete_medicine(request, pk):
    if not request.user.is_superuser:
        return redirect('login')
    
    medicine = get_object_or_404(Medicine, pk=pk)
    medicine.delete()
    return redirect('admin_dashboard:medicine_list')  

@login_required
def logout_user(request):
    logout(request)
    return redirect('login_register:onboarding')

@login_required
def order_list(request):
    if not request.user.is_superuser:
        return redirect('login')  # Redirect non-admins to the login page
    
    # Get all orders in the database, ordered by creation date (newest first)
    orders = Order.objects.all().order_by('-created_at')
    
    return render(request, 'admin_dashboard/order_list.html', {'orders': orders})

@login_required
def order_details(request, order_id):
    if not request.user.is_superuser:
        return redirect('login')  # Redirect non-admins to the login page
    
    # Fetch the order by ID or return a 404 if it doesn't exist
    order = get_object_or_404(Order, id=order_id)

    return render(request, 'admin_dashboard/customer_order_details.html', {'order': order})

@login_required
def customer_list(request):
    if not request.user.is_superuser:
        return redirect('login')
    
    # Fetch superusers and non-superuser customers
    superusers = User.objects.filter(is_superuser=True).order_by('id')  
    customers = User.objects.filter(is_superuser=False).order_by('id')  
    
    return render(request, 'admin_dashboard/customer_list.html', {'superusers': superusers, 'customers': customers})

@login_required
def customer_details(request, customer_id):
    if not request.user.is_superuser:
        return redirect('login')

    customer = get_object_or_404(User, id=customer_id)
    return render(request, 'admin_dashboard/customer_details.html', {'customer': customer})

@login_required
def delete_customer(request, customer_id):
    if not request.user.is_superuser:
        return redirect('login')
    
    customer = get_object_or_404(User, id=customer_id)
    customer.delete()
    return redirect('admin_dashboard:customer_list')