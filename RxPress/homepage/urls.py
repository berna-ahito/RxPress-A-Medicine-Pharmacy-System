from django.urls import path
from . import views

app_name = 'homepage'

urlpatterns = [
    path('homepage/', views.homepage, name='homepage'),  # Display medicines
    path('cart/', views.cart_view, name='cart_view'),
    path('order/', views.order_view, name='order_view'),
    path('logout/', views.logout_view, name='logout'),
]
