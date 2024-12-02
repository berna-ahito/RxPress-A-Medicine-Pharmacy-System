from django.urls import path
from . import views

app_name = 'login_register'

urlpatterns = [
    path('', views.splash, name='splash'),
    path('onboarding/', views.onboarding, name='onboarding'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('homepage/', views.homepage, name='homepage'),

]
