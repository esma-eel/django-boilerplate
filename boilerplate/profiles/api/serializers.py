from boilerplate.common.utils.number_helpers import ir_phone_number
from rest_framework import serializers
from boilerplate.profiles.models import (
    ProfilePhoneNumber,
    ProfileEmail,
    ProfileAddress,
    Profile,
)


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)

    def validate_phone_number(self, value):
        if not ir_phone_number(value):
            raise serializers.ValidationError(
                {"phone_number": "Phone number is not valid"}
            )

        return value


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ProfilePhoneNumberModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilePhoneNumber
        fields = [
            "phone_number",
            "is_primary",
            "is_verified",
        ]
        extra_kwargs = {
            "is_primary": {
                "required": True,
                "allow_null": False,
            },
            "is_verified": {"read_only": True},
        }

    def validate_phone_number(self, value):
        if not ir_phone_number(value):
            raise serializers.ValidationError(
                {"phone_number": "Phone number is not valid"}
            )

        return value


class ProfileEmailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileEmail
        fields = [
            "email",
            "is_primary",
            "is_verified",
        ]
        extra_kwargs = {
            "is_primary": {
                "required": True,
                "allow_null": False,
            },
            "is_verified": {"read_only": True},
        }


class ProfileAddressModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileAddress
        fields = [
            "city",
            "address",
            "is_primary",
        ]
        extra_kwargs = {
            "is_primary": {
                "required": True,
                "allow_null": False,
            }
        }


class ProfileModelSerializer(serializers.ModelSerializer):
    phone_numbers = ProfilePhoneNumberModelSerializer(
        source="phone_number_set",
        many=True,
        required=False,
    )
    emails = ProfileEmailModelSerializer(
        source="email_set",
        many=True,
        required=False,
    )
    addresses = ProfileAddressModelSerializer(
        source="address_set",
        many=True,
        required=False,
    )

    class Meta:
        model = Profile
        fields = [
            "name",
            "avatar",
            "phone_numbers",
            "emails",
            "addresses",
        ]
        extra_kwargs = {
            "name": {
                "required": True,
                "allow_blank": False,
                "allow_null": False,
            }
        }
