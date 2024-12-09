# Generated by Django 5.0.1 on 2024-12-05 04:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_dashboard', '0004_initial'),
        ('orders', '0002_alter_order_cart_orderitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='medicine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='admin_dashboard.medicine'),
        ),
    ]
