from django.urls import path, include
from . import views  # Import your views

app_name = 'homepage'  # Namespacing the app URLs

urlpatterns = [

    path('homepage/', views.homepage, name='homepage'),  # Homepage route
    path('order/', views.order_view, name='order_view'),  # Example route
    path('cart/', views.cart_view, name='cart_view'),
    path('logout/', views.logout, name='logout'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),


]
