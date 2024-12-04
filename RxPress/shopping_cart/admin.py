from django.contrib import admin
from .models import Cart, CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_total_quantity', 'total_cost')  # Updated fields
    search_fields = ('user__username',)  # Search by user
    list_filter = ('user',)

    # Custom method to get the total quantity from the related CartItems
    def get_total_quantity(self, obj):
        return sum(item.quantity for item in obj.cartitems.all())  # Adjust according to your relation
    get_total_quantity.short_description = 'Total Quantity'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'medicine', 'quantity', 'total_cost')  # Fields displayed in the list view
    search_fields = ('medicine__name',)  # Search by medicine name
    list_filter = ('cart',)  # Add filtering by cart
