from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_cost', 'get_total_quantity', 'get_item_cost')  # Updated fields
    search_fields = ('user__username',)  # Search by user's username
    list_filter = ('user',)  # Filter by user

    # Custom method to get the total quantity from the related CartItems
    def get_total_quantity(self, obj):
        return sum(item.quantity for item in obj.cart.cartitems.all())  # Adjust according to your relation
    get_total_quantity.short_description = 'Total Quantity'

    # Custom method to get the total item cost from the related CartItems
    def get_item_cost(self, obj):
        return sum(item.total_cost for item in obj.cart.cartitems.all())  # Adjust according to your relation
    get_item_cost.short_description = 'Total Item Cost'
