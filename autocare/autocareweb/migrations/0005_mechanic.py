# Generated by Django 5.1 on 2024-10-08 08:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autocareweb', '0004_allocatedmanager'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mechanic',
            fields=[
                ('mechanic_id', models.AutoField(primary_key=True, serialize=False)),
                ('level', models.CharField(choices=[('senior', 'Senior Level'), ('medium', 'Medium Level'), ('entry', 'Entry Level')], default='entry', max_length=10)),
                ('status', models.CharField(choices=[('working', 'Working'), ('active', 'Active'), ('absentees', 'Absentees')], default='active', max_length=10)),
                ('mechanic_email', models.ForeignKey(limit_choices_to={'role': 'mechanic'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
