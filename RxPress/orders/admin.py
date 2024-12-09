from django.contrib import admin
from .models import Order, OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_cost', 'get_total_quantity', 'get_item_cost', 'created_at') 
    search_fields = ('user__username',)  
    list_filter = ('user',) 

    def get_total_quantity(self, obj):
        return sum(item.quantity for item in obj.items.all())  # Accessing OrderItems directly
    get_total_quantity.short_description = 'Total Quantity'

    def get_item_cost(self, obj):
        return sum(item.item_cost for item in obj.items.all())  # Accessing OrderItems directly
    get_item_cost.short_description = 'Total Item Cost'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'medicine', 'quantity', 'item_cost')
    search_fields = ('order__user__username', 'medicine__name')  # You can search by order's user and medicine's name
    list_filter = ('medicine',)  # Allows filtering by medicine type
