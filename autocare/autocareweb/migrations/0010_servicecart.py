# Generated by Django 5.1 on 2024-10-13 14:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autocareweb', '0009_servicecategory_image_servicetype_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('service_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocareweb.servicetype')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='autocareweb.vehicle')),
            ],
        ),
    ]
