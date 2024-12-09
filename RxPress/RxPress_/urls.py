
"""
URL configuration for RxPress_ project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login_register.urls')),
    path('admin-dashboard/', include('admin_dashboard.urls')),
    path('homepage/', include('homepage.urls')),
    path('cart/', include('shopping_cart.urls', namespace='shopping_cart')),
    path('order/', include('orders.urls', namespace='orders')),
    path('profile_management/', include('profile_management.urls', namespace='profile_management')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



