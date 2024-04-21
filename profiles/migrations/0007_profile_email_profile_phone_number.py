# Generated by Django 4.2.6 on 2024-01-11 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0006_remove_profile_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email'),
        ),
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=11, null=True, verbose_name='Phone Number'),
        ),
    ]