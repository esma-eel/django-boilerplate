# from rest_framework import serializers
from boilerplate.profiles.api.serializers import (
    PhoneNumberSerializer,
    EmailSerializer,
)
from boilerplate.authentication.api.password.serializers import (
    PasswordSerializer,
)


class PhonePasswordSerializer(PhoneNumberSerializer, PasswordSerializer):
    pass


class EmailPasswordSerializer(EmailSerializer, PasswordSerializer):
    pass
