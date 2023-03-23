# Generated by Django 4.1.7 on 2023-03-21 09:32

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0006_remove_user_data_access_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_data',
            name='access_token',
            field=models.CharField(default=django.utils.timezone.now, max_length=500),
            preserve_default=False,
        ),
    ]
