from django.db import models
from django.contrib.auth.models import User
from admin_dashboard.models import Medicine

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shopping_cart')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    def __str__(self):
        return f"{self.user.username}'s cart"
    
    def update_total_cost(self):
        self.total_cost = sum(item.total_cost for item in self.cartitems.all())  
        self.save()

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitems')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0.00) 

    def save(self, *args, **kwargs):
        self.total_cost = self.medicine.price * self.quantity  
        super().save(*args, **kwargs)
        self.cart.update_total_cost() 

    def __str__(self):
        return f"{self.medicine.name} in {self.cart.user.username}'s cart"


