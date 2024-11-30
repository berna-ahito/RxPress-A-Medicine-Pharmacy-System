from django.contrib import admin
from .models import UserProfile

# Register the UserProfile model to the Django admin interface
admin.site.register(UserProfile)
