# Generated by Django 4.2.6 on 2023-10-17 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profileaddress',
            name='is_primary',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profileemail',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profilephonenumber',
            name='is_verified',
            field=models.BooleanField(default=False),
        ),
    ]