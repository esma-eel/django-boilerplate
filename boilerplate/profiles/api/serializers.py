from boilerplate.common.utils.number_helpers import ir_phone_number
from rest_framework import serializers


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
