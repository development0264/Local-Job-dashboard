# Generated by Django 4.1.7 on 2023-03-20 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_name', models.CharField(max_length=1000, null=True)),
                ('job_location', models.CharField(max_length=1000, null=True)),
                ('address', models.CharField(max_length=1000, null=True)),
                ('contact', models.CharField(max_length=1000, null=True)),
                ('pin_code', models.CharField(max_length=1000, null=True)),
                ('budget', models.CharField(max_length=1000, null=True)),
                ('verified_account', models.BooleanField(default=True)),
            ],
        ),
    ]