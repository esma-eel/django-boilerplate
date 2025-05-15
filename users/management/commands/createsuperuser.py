from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model

class Command(createsuperuser.Command):
    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            '--name',
            dest='name',
            default=None,
            help='The name of the superuser.',
        )
        parser.add_argument(
            '--email',
            dest='email',
            default=None,
            help='The email address of the superuser.',
        )

    def handle(self, *args, **options):
        if not options.get('username'):
            options['username'] = input("Username: ")

        name = options.get('name')
        email = options.get('email')
        if not name:
            name = input("Name: ")
        if not email:
            email = input("Email: ")

        super().handle(*args, **options)
        User = get_user_model()
        user = User.objects.get(username=options['username'])
        user.profile.name = name 
        user.profile.email = email 
        user.profile.save()
        print("Profile created and updated too.")
