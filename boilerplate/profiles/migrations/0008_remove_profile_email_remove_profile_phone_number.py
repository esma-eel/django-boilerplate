# Generated by Django 4.2.6 on 2024-01-11 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0007_profile_email_profile_phone_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='phone_number',
        ),
    ]