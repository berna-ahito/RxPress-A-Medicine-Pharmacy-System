from django.urls import path
from . import views

app_name = 'shopping_cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),  # Update to match the existing view
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('remove_from_cart/', views.remove_from_cart, name='remove_from_cart'),
    path('place_order/', views.place_order, name='place_order'),
]
