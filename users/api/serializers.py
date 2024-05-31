from rest_framework import serializers
from django.contrib.auth import get_user_model
from profiles.api.serializers import (
    ProfileModelSerializer,
    PhoneNumberSerializer,
    EmailSerializer,
)
from authentication.api.password.serializers import (
    PasswordCheckSerializer,
)

User = get_user_model()


class UserModelSerializer(serializers.ModelSerializer):
    profile = ProfileModelSerializer()

    class Meta:
        model = User
        fields = ["username", "is_staff", "profile"]


class CreateUserModelSerializer(serializers.Serializer):
    user = UserModelSerializer()
    authentication = PasswordCheckSerializer()


class RegisterUserSerilaizer(PhoneNumberSerializer, EmailSerializer):
    username = serializers.CharField(max_length=32)
    name = serializers.CharField()
    authentication = PasswordCheckSerializer()


"""
{
    "user": {
        "username": "esmaeel",
    },
    "authentication": {
        "password": "12345",
        "repeat_password": "..."
    },
    "profile": {
        "name": "Esmaeel Komijani",
        "phone_numbers": [
            {
                "phone_number": "12345",
                "is_primary": True
            }
        ],
        "emails": [
            {
                "email": "verygood@gm.com",
                "is_primary": True
            }
        ],
        "address": [
            {
                "address": "",
                "city": "",
                "is_primary": ""
            }
        ]
    }
}
"""
