# Generated by Django 5.0.1 on 2024-12-03 17:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('homepage', '0005_remove_cart_medicine_remove_cart_user_and_more'),
        ('shopping_cart', '0007_alter_cartitem_medicine'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Medicine',
        ),
    ]
