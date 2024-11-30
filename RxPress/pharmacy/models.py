from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    
    
class Order(models.Model):
    name = models.CharField(max_length=255)
    quantity = models.PositiveIntegerField()
    item_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
    

# class Cart(models.Model):
#     medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()

#     def __str__(self):
#         return f"{self.medicine.name} - {self.quantity}"
 
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.medicine.name} - {self.quantity}"
    

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.total_cost = self.medicine.price * self.quantity  # Recalculate the total cost
        super().save(*args, **kwargs)
        self.cart.update_total_cost()  # Update total cost in the associated cart

    def __str__(self):
        return f"{self.medicine.name} in {self.cart.user.username}'s cart"

    

    
   