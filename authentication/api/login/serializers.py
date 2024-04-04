# from rest_framework import serializers
from profiles.api.serializers import (
    PhoneNumberSerializer,
    EmailSerializer,
)
from authentication.api.password.serializers import (
    PasswordSerializer,
)


class PhonePasswordSerializer(PhoneNumberSerializer, PasswordSerializer):
    pass


class EmailPasswordSerializer(EmailSerializer, PasswordSerializer):
    pass
