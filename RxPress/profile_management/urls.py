from django.urls import path
from . import views

app_name = 'profile_management'

urlpatterns = [
    path('profile/', views.profile_view, name='profile_view'),
    path('account/', views.account, name='account'),
    path('edit/', views.edit_profile, name='edit_profile'),
]
