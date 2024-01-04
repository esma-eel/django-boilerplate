from rest_framework import serializers
from boilerplate.common.api.general.serializers import (
    PhoneNumberSerializer,
    EmailSerializer,
)


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField()


class PhonePasswordSerializer(
    PhoneNumberSerializer, PasswordSerializer, serializers.Serializer
):
    pass


class EmailPasswordSerializer(
    EmailSerializer, PasswordSerializer, serializers.Serializer
):
    pass
