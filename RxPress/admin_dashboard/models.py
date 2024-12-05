from django.db import models
from login_register.models import User 

class Medicine(models.Model):
<<<<<<< HEAD
    medicine_id = models.CharField(max_length=10, unique=True, null=False)  # Unique medicine identifier
    name = models.CharField(max_length=255, unique=True, null=False)
=======
    name = models.CharField(max_length=100)
>>>>>>> 0351f593192c0c46ce4d7da1e262560c46c990bf
    description = models.TextField()
    strength = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
<<<<<<< HEAD
    quantity = models.PositiveIntegerField()
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_medicines')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_medicines')
    deleted_at = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)
=======
    quantity = models.PositiveIntegerField() 
>>>>>>> 0351f593192c0c46ce4d7da1e262560c46c990bf

    def __str__(self):
        return f"{self.medicine_id} - {self.name}"