from django.contrib import admin
from .models import CartItem

class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'medicine', 'quantity', 'total_price')  # Ensure 'user' and 'total_price' are valid
    list_filter = ('user',)

    # If 'total_price' is not a field on the model, define it as a method
    def total_price(self, obj):
        return obj.medicine.price * obj.quantity
    total_price.admin_order_field = 'total_price'  # Make it sortable
    total_price.short_description = 'Total Price'

admin.site.register(CartItem, CartItemAdmin)
