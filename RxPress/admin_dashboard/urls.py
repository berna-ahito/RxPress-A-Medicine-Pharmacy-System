from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.medicine_list, name='medicine_list'),
    path('add/', views.add_medicine, name='add_medicine'),
    path('update_medicine/<int:pk>/', views.update_medicine, name='update_medicine'),
    path('delete/<int:pk>/', views.delete_medicine, name='delete_medicine'), 
    path('logout_user/', views.logout_user, name='logout_user'),
    path('order_list/', views.order_list, name='order_list'),
    path('orders/<int:order_id>/', views.order_details, name='order_details'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/<int:customer_id>/', views.customer_details, name='customer_details'),
    path('customers/<int:customer_id>/delete/', views.delete_customer, name='delete_customer'),
]

