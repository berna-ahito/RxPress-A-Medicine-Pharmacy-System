from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'admin_dashboard'

urlpatterns = [
    path('add_medicine/', views.add_medicine, name='add_medicine'),  
    path('medicine_list/', views.medicine_list, name='medicine_list'), 
    path('logout/', LogoutView.as_view(), name='logout'),
]
