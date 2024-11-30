# from django.urls import path
# from . import views

# app_name = 'pharmacy'

# urlpatterns = [
#     path('', views.homepage, name='homepage'),
#     path('order', views.order_view, name='order_view'),
    

# ]

from django.urls import path
from . import views  # Import your views

app_name = 'pharmacy'  # Namespacing the app URLs

urlpatterns = [
    path('', views.homepage, name='homepage'),  # Homepage route
    path('order/', views.order_view, name='order_view'),  # Example route
    path('cart/', views.cart_view, name='cart_view'),
    # path('add_to_cart/', views.add_to_cart, name='add_to_cart'),  # Add to Cart
    
]
