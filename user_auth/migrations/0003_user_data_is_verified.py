# Generated by Django 4.1.7 on 2023-03-20 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0002_alter_user_data_work_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_data',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]
