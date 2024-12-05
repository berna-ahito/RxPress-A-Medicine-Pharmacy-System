from django.urls import path
from . import views

app_name = 'shopping_cart'

urlpatterns = [
    path('', views.cart_view, name='cart_view'),
    path('update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('place-order/', views.place_order, name='place_order'),  # Add this line
    path('order-confirmation/', views.order_confirmation, name='order_confirmation'),
]
