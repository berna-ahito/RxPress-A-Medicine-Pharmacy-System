from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('order/', views.order_view, name='order_view'),
    path('checkout/', views.checkout, name='checkout'),
]
