from django.db import models

from django.db import models

# Medicine Model
class Medicine(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    strength = models.CharField(max_length=50)
    category = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()  # Prevents negative quantities

    def __str__(self):
        return self.name
