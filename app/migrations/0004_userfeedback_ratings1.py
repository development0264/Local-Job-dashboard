# Generated by Django 4.1.7 on 2023-03-21 05:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_job_verified_account_userfeedback_bidforjob'),
    ]

    operations = [
        migrations.AddField(
            model_name='userfeedback',
            name='ratings1',
            field=models.IntegerField(default=1, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)]),
        ),
    ]