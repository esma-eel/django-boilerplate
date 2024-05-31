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


class RegisterUserModelSerializer(UserModelSerializer):
    class Meta:
        model = User
        fields = ["username", "profile"]


class CreateUserModelSerializer(serializers.Serializer):
    user = UserModelSerializer()
    authentication = PasswordCheckSerializer()


class RegisterUserSerilaizer(CreateUserModelSerializer):
    user = RegisterUserModelSerializer()
