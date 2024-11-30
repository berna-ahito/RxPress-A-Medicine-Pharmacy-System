from django.shortcuts import render, redirect
from .models import Medicine
from .forms import MedicineForm
from django.template import TemplateDoesNotExist, loader

# View to display the list of medicines
def medicine_list(request):
    try:
        template = loader.get_template('medicine_list.html')
    except TemplateDoesNotExist:
        print("Template not found")
        raise
    return render(request, 'medicine_list.html')

# View to handle adding a new medicine
def add_medicine(request):
    if request.method == 'POST':
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new medicine to the database
            return redirect('medicine_list')  # Redirect to the medicine list view
    else:
        form = MedicineForm()
    
    return render(request, 'add_medicine.html', {'form': form})

def admin_dashboard(request):
    return render(request, 'medicine_list.html')

def medicine_list(request):
    # Fetch all medicines from the database
    medicines = Medicine.objects.all()
    # Pass the medicines to the template
    return render(request, 'medicine_list.html', {'medicines': medicines})
