from django.contrib import admin
from .models import Cart, CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_total_quantity', 'total_cost')  
    search_fields = ('user__username',) 
    list_filter = ('user',)

    def get_total_quantity(self, obj):
        return sum(item.quantity for item in obj.cartitems.all())  
    get_total_quantity.short_description = 'Total Quantity'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'medicine', 'quantity', 'total_cost') 
    search_fields = ('medicine__name',)
    list_filter = ('cart',)  
