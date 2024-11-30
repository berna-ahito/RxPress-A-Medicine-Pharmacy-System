# Generated by Django 5.1.3 on 2024-11-30 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Medicine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('description', models.TextField()),
                ('strength', models.CharField(max_length=50)),
                ('category', models.CharField(choices=[('Antibiotic', 'Antibiotic'), ('Pain Reliever', 'Pain Reliever'), ('Vitamins', 'Vitamins'), ('Antiseptic', 'Antiseptic'), ('Others', 'Others')], max_length=50)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('quantity', models.PositiveIntegerField()),
            ],
        ),
    ]
