# Generated by Django 5.1 on 2024-10-20 20:01

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autocareweb', '0015_order_orderservice'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicecart',
            name='cart_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]