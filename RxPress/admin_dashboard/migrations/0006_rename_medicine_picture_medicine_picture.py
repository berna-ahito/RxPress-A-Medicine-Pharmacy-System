# Generated by Django 5.1.3 on 2024-12-08 10:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_dashboard', '0005_medicine_medicine_picture'),
    ]

    operations = [
        migrations.RenameField(
            model_name='medicine',
            old_name='medicine_picture',
            new_name='picture',
        ),
    ]