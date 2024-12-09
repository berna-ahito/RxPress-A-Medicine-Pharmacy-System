from django.db import models
from django.contrib.auth.models import User
from shopping_cart.models import Cart

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True) 
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

    def calculate_total_cost(self):
        return sum(item.item_cost for item in self.items.all())  

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    medicine = models.ForeignKey('admin_dashboard.Medicine', on_delete=models.CASCADE)  
    quantity = models.PositiveIntegerField()
    item_cost = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} of {self.medicine.name} - ₱{self.item_cost}"
