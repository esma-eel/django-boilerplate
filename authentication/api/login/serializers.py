# from rest_framework import serializers
from profiles.api.serializers import (
    EmailReceiverSerializer,
    PhoneNumberReceiverSerializer,
)
from authentication.api.password.serializers import (
    PasswordSerializer,
)


class PhonePasswordSerializer(PhoneNumberReceiverSerializer, PasswordSerializer):
    pass


class EmailPasswordSerializer(EmailReceiverSerializer, PasswordSerializer):
    pass
