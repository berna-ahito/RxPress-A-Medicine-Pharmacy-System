from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'admin_dashboard'

urlpatterns = [
<<<<<<< HEAD
    path('medicine_list', views.medicine_list, name='medicine_list'),
    path('add_medicine/', views.add_medicine, name='add_medicine'),
    path('medicine_list/', views.medicine_list, name='medicine_list'),
    path('logout/', views.logout_user, name='logout_user'),
=======
    path('add_medicine/', views.add_medicine, name='add_medicine'),  
    path('medicine_list/', views.medicine_list, name='medicine_list'), 
    path('logout/', LogoutView.as_view(), name='logout'),
>>>>>>> 0351f593192c0c46ce4d7da1e262560c46c990bf
]
