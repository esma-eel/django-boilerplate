# Generated by Django 4.2.6 on 2024-01-11 16:00

import boilerplate.users.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_user_email'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', boilerplate.users.models.UserManager()),
            ],
        ),
    ]
