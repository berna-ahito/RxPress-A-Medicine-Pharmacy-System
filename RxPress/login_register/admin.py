from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_superuser')
    search_fields = ('username', 'email')
    list_filter = ('is_superuser',)
    ordering = ('username',)
