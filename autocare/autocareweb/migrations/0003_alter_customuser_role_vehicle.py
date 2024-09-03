# Generated by Django 5.1 on 2024-09-03 15:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autocareweb', '0002_userdetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('service_manager', 'ServiceManager'), ('mechanic', 'Mechanic'), ('customer', 'Customer')], default='customer', max_length=20),
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_type', models.CharField(choices=[('car', 'Car'), ('bike', 'Bike')], max_length=10)),
                ('vehicle_brand', models.CharField(max_length=50)),
                ('vehicle_variant', models.CharField(max_length=50)),
                ('vehicle_number', models.CharField(max_length=20, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicles', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
