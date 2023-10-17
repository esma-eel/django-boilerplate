from rest_framework import serializers
from boilerplate.common.utils.numbers import ir_phone_number


class PhoneNumberAndPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    password = serializers.CharField()

    def validate_phone_number(self, value):
        if not ir_phone_number(value):
            raise serializers.ValidationError(
                {"phone_number": "Phone number is not valid"}
            )

        return value
