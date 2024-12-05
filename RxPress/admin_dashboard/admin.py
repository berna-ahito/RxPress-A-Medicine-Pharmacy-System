from django.contrib import admin
from .models import Medicine  

class MedicineAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'strength', 'price', 'quantity']
    search_fields = ['name', 'category']
    
admin.site.register(Medicine, MedicineAdmin) 
