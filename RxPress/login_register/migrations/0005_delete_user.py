# Generated by Django 5.1.3 on 2024-12-08 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login_register', '0004_user_delete_customuser'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
