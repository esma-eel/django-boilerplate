# Generated by Django 4.2.6 on 2024-01-11 15:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_alter_profilephonenumber_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='uuid',
        ),
    ]
