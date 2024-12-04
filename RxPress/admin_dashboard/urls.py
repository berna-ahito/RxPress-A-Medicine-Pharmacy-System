from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'admin_dashboard'

urlpatterns = [
    path('add_medicine/', views.add_medicine, name='add_medicine'),  # URL for adding medicine
    path('medicine_list/', views.medicine_list, name='medicine_list'),  # URL for listing medicines
    path('logout/', LogoutView.as_view(), name='logout'),
]
