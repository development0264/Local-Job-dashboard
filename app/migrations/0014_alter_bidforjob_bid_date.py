# Generated by Django 4.1.7 on 2023-03-24 12:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_alter_bidforjob_bid_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bidforjob',
            name='bid_date',
            field=models.DateField(default=datetime.datetime.now, null=True),
        ),
    ]
