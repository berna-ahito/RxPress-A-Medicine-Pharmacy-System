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


# Order Model
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='orders')
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    is_cart = models.BooleanField(default=True)  # Distinguishes between cart items and orders
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.total_cost = self.medicine.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.medicine.name} - {'Cart' if self.is_cart else 'Order'}"


# User Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    userID = models.PositiveIntegerField(null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    password = models.CharField(max_length=50, null=True, blank=True)
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]
    user_type = models.CharField(max_length=5, choices=USER_TYPE_CHOICES, default='user')

    def __str__(self):
        return f'{self.first_name or "No Name"} ({self.user.username})'

    def save(self, *args, **kwargs):
        if not self.userID and self.user:
            self.userID = self.user.id
        super().save(*args, **kwargs)


# Signals to Create and Update User Profile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# Shopping Cart Model
class ShoppingCart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shopping_cart')
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Cart for {self.user.username}"

    def update_total_cost(self):
        """Update the total cost of the cart."""
        self.total_cost = sum(item.total_cost for item in self.items.all())
        self.save()


class CartItem(models.Model):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.total_cost = self.medicine.price * self.quantity  # Recalculate the total cost
        super().save(*args, **kwargs)
        self.cart.update_total_cost()  # Update total cost in the associated cart

    def __str__(self):
        return f"{self.medicine.name} in {self.cart.user.username}'s cart"

