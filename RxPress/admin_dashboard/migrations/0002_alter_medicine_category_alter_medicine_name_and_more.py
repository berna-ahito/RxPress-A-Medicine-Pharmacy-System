# Generated by Django 5.1.3 on 2024-11-30 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicine',
            name='category',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='medicine',
            name='strength',
            field=models.CharField(max_length=255),
        ),
    ]