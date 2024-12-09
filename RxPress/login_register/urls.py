from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'login_register'

urlpatterns = [
    path('', views.splash, name='splash'),
    path('onboarding/', views.onboarding, name='onboarding'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
