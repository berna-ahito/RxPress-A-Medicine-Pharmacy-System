from django.contrib import admin
from .models import Medicine

class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name','description', 'category', 'strength', 'price', 'quantity')
    search_fields = ('name', 'category')
    list_filter = ('category',)
