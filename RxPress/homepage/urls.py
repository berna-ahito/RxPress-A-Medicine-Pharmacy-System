from django.urls import path
from . import views

app_name = 'homepage'

urlpatterns = [
    path('homepage/', views.homepage, name='homepage'),  # Display medicines
    path('cart/', views.cart_view, name='cart_view'),
    path('order/', views.order_view, name='order_view'),
    path('product-details/<int:product_id>/', views.product_details, name='product_details'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('logout_user/', views.logout_user, name='logout_user'),
]
