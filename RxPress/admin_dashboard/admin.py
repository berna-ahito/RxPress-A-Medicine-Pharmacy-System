# admin_dashboard/admin.py

from django.contrib import admin
from .models import Medicine  # Import the model from admin_dashboard.models

class MedicineAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'strength', 'price', 'quantity']
    search_fields = ['name', 'category']
    
admin.site.register(Medicine, MedicineAdmin)  # Register the model with the admin
