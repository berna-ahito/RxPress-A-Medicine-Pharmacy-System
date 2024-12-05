# Generated by Django 5.1.3 on 2024-12-05 15:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('username', models.CharField(max_length=255, unique=True)),
                ('email', models.EmailField(default='default@example.com', max_length=254, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('isAdmin', models.BooleanField(default=False)),
            ],
        ),
    ]
