from django.contrib import admin
from .models import Medicine, Order, Profile, ShoppingCart, CartItem


# Customize the Medicine Admin Interface
@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'strength', 'category', 'price', 'quantity')  # Columns to display in the admin list view
    search_fields = ('name', 'category')  # Searchable fields
    list_filter = ('category',)  # Filters for the admin interface
    ordering = ('name',)  # Default ordering


# Customize the Order Admin Interface
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('medicine', 'quantity', 'order_date', 'is_cart', 'total_cost')  # Columns to display
    list_filter = ('is_cart', 'order_date')  # Filters for cart status and order date
    search_fields = ('medicine__name',)  # Enable search by medicine name
    ordering = ('-order_date',)  # Default ordering (most recent orders first)


# Customize the Profile Admin Interface
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'user_type')  # Columns to display
    list_filter = ('user_type',)  # Filters for user types
    search_fields = ('user__username', 'first_name')  # Enable search by username or first name
    ordering = ('user',)


# Customize the ShoppingCart Admin Interface
@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_cost')  # Columns to display
    search_fields = ('user__username',)  # Enable search by username
    ordering = ('user',)


# Customize the CartItem Admin Interface
@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'medicine', 'quantity', 'total_cost')  # Columns to display
    search_fields = ('cart__user__username', 'medicine__name')  # Enable search by cart user or medicine name
    ordering = ('cart', 'medicine')  # Default ordering
