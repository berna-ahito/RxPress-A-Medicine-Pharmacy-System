from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Medicine Model
class Medicine(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    strength = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name


# Modify Order model to have total cost
class Order(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    is_cart = models.BooleanField(default=True)  # Distinguishes cart items from placed orders
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # Total cost per item

    def save(self, *args, **kwargs):
        # Automatically update total cost whenever the quantity or medicine price changes
        self.total_cost = self.medicine.price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.medicine.name} ({'Cart' if self.is_cart else 'Order'})"


# Profile Model
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # New fields with defaults
    userID = models.IntegerField(null=True, blank=True)  # Allow null values
    firstName = models.CharField(max_length=255, null=True, blank=True)  # Allow null values
    username = models.CharField(max_length=50, unique=True)  # Username as VARCHAR(50), unique
    password = models.CharField(max_length=50, null=True, blank=True)  # Allow null values
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('user', 'User'),
    ]
    # Set default value for 'user_type' to avoid issues with non-nullable constraint
    user_type = models.CharField(max_length=5, choices=USER_TYPE_CHOICES, default='user')  # Default set to 'user'

    def __str__(self):
        return f'{self.firstName} ({self.username}) Profile'

    # Ensure userID is set after the profile is created
    def save(self, *args, **kwargs):
        if not self.userID and self.user:
            self.userID = self.user.id  # Set userID to User's id
        super().save(*args, **kwargs)


# Signals to auto-create and update user profile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class ShoppingCart(models.Model):
    cartID = models.AutoField(primary_key=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shopping_cart')

    def __str__(self):
        return f"Cart for {self.user.username}"

# CartItem Model to link the shopping cart and medicines
class CartItem(models.Model):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.medicine.name} in {self.cart.user.username}'s cart"