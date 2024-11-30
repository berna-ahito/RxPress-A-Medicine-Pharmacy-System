from django.conf import settings
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # other fields...
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    # additional fields...
    
    def __str__(self):
        return self.user.username
