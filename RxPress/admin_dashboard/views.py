from django.shortcuts import render, redirect
from admin_dashboard.models import Medicine
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
