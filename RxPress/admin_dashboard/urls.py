from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('medicine_list', views.medicine_list, name='medicine_list'),
    path('add_medicine/', views.add_medicine, name='add_medicine'),
    path('medicine_list/', views.medicine_list, name='medicine_list'),
    path('logout/', views.logout_user, name='logout_user'),
]
