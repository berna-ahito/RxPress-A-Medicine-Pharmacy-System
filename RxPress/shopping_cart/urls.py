# shopping_cart/urls.py

from django.urls import path
from . import views

app_name = 'shopping_cart'

urlpatterns = [
    path('cart/', views.cart_view, name='cart_view'),
    path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
]
