from django.db import transaction
from common.utils.number_helpers import ir_phone_number
from rest_framework import serializers
from profiles.models import Profile


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)

    def validate_phone_number(self, value):
        if not ir_phone_number(value):
            raise serializers.ValidationError(
                {"phone_number": "Phone number is not valid"}
            )

        return value


class PhoneNumberReceiverSerializer(PhoneNumberSerializer):

    def validate_phone_number(self, value):
        super().validate_phone_number(value)

        qs = Profile.objects.filter(phone_number=value)
        if not qs.exists():
            raise serializers.ValidationError(
                {"phone_number": "phone number is not found/verified"}
            )

        return value


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class EmailReceiverSerializer(EmailSerializer):
    def validate_email(self, value):
        qs = Profile.objects.filter(email=value)
        if not qs.exists():
            raise serializers.ValidationError(
                {"email": "email is not found/verified"}
            )

        return value


class ProfileModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "name",
            "avatar",
            "phone_number",
            "email",
            "city",
            "address",
        ]
        extra_kwargs = {
            "name": {
                "required": True,
                "allow_blank": False,
                "allow_null": False,
            },
            "phone_number": {
                "required": True,
                "allow_blank": False,
                "allow_null": False,
            },
            "email": {
                "required": True,
                "allow_blank": False,
                "allow_null": False,
            },
            "city": {
                "required": True,
                "allow_blank": False,
                "allow_null": False,
            },
            "address": {
                "required": True,
                "allow_blank": False,
                "allow_null": False,
            },
        }
