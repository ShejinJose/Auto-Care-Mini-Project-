# Generated by Django 5.1 on 2024-10-21 16:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autocareweb', '0018_order_allocated_slot'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slot',
            name='mechanic',
            field=models.ForeignKey(blank=True, limit_choices_to={'role': 'mechanic'}, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
