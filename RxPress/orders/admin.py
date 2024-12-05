from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_cost', 'get_total_quantity', 'get_item_cost') 
    search_fields = ('user__username',)  
    list_filter = ('user',) 

    def get_total_quantity(self, obj):
        return sum(item.quantity for item in obj.cart.cartitems.all())  
    get_total_quantity.short_description = 'Total Quantity'

    def get_item_cost(self, obj):
        return sum(item.total_cost for item in obj.cart.cartitems.all()) 
    get_item_cost.short_description = 'Total Item Cost'
