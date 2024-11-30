from django.urls import path
from . import views

app_name = 'profile_management'

urlpatterns = [
    path('profile/', views.profile_view, name='profile_view'),  # Corrected path to profile_view
    path('account/', views.account, name='account'),  # Edit profile page
]
