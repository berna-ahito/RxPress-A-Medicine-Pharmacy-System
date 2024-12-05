from django.db import models
class User(models.Model):
    first_name = models.CharField(max_length=255, null=False)
    last_name = models.CharField(max_length=255, null=False)
    username = models.CharField(max_length=255, unique=True, null=False)
    email = models.EmailField(unique=True, null=False, default='default@example.com')
    password = models.CharField(max_length=128, null=False)
    is_superuser = models.BooleanField(default=False)

    def __str__(self):
        return self.username
