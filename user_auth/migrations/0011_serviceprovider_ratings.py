# Generated by Django 4.1.7 on 2023-03-31 12:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0010_remove_user_data_work_field_serviceprovider'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceprovider',
            name='ratings',
            field=models.FloatField(default=3, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)]),
        ),
    ]
