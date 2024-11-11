from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'pharmacy'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('cart/', views.cart_view, name='cart_view'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('place-order/', views.place_order, name='place_order'),
    path('login/', auth_views.LoginView.as_view(template_name='pharmacy/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('account/', views.account_view, name='account'),
    path('edit-account/', views.edit_account, name='edit_account'),  # New route for editing account
]
