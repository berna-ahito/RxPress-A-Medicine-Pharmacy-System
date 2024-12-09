from django.urls import path
from . import views

app_name = 'profile_management'

urlpatterns = [
    path('account/', views.account, name='account'),  
    path('edit-profile/', views.edit_profile, name='edit_profile'),  
    path('profile-view/', views.profile_view, name='profile_view'),  
    path('logout_user/', views.logout_user, name='logout_user'),
]
