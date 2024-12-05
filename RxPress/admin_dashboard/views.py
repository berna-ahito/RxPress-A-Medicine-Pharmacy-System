from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Medicine
from .forms import MedicineForm
from django.contrib import messages

def add_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new medicine to the database
            messages.success(request, "Medicine added!")  # Success message
            return redirect('admin_dashboard:medicine_list')  # Redirect to the medicine list after adding
    else:
        form = MedicineForm()

    return render(request, 'add_medicine.html', {'form': form})

def medicine_list(request):
    medicines = Medicine.objects.all()  # Fetch all medicines from the database
    return render(request, 'medicine_list.html', {'medicines': medicines})

def admin_dashboard(request):
    return render(request, 'medicine_list.html')

def update_medicine(request, id):
    if request.method == 'POST':
        medicine = get_object_or_404(Medicine, id=id)
        data = request.POST
        
        medicine.name = data.get('name', medicine.name)
        medicine.description = data.get('description', medicine.description)
        medicine.strength = data.get('strength', medicine.strength)
        medicine.category = data.get('category', medicine.category)
        medicine.price = data.get('price', medicine.price)
        medicine.quantity = data.get('quantity', medicine.quantity)
        medicine.save()

        return JsonResponse({'success': 'Medicine updated successfully!'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

def delete_medicine(request, id):
    medicine = get_object_or_404(Medicine, id=id)
    medicine.delete()
    messages.success(request, "Medicine deleted successfully!")
    return redirect('admin_dashboard')

def logout_user(request):
    logout(request)
    return redirect('login_register:login')
