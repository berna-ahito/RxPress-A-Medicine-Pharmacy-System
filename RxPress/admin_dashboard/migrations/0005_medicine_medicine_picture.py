# Generated by Django 5.1.3 on 2024-12-08 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_dashboard', '0004_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicine',
            name='medicine_picture',
            field=models.ImageField(blank=True, null=True, upload_to='medicine_images/'),
        ),
    ]
