from django.db import models

class Medicine(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    strength = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()  # Prevents negative quantities
    picture = models.ImageField(upload_to='medicine_images/', blank=True, null=True)

    def __str__(self):
        return self.name
