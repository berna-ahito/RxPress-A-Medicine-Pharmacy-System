from django.db import models

class Medicine(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False)
    description = models.TextField()
    strength = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name
