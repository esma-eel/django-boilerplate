from rest_framework import serializers
from boilerplate.common.utils.numbers import ir_phone_number
from rest_framework_simplejwt.tokens import RefreshToken, SlidingToken
from rest_framework_simplejwt.serializers import TokenBlacklistSerializer


class PhoneNumberAndPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    password = serializers.CharField()

    def validate_phone_number(self, value):
        if not ir_phone_number(value):
            raise serializers.ValidationError(
                {"phone_number": "Phone number is not valid"}
            )

        return value


class EmailAndPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class JWTTokenBlacklistSerializer(TokenBlacklistSerializer):
    token_class = RefreshToken


class SlidingTokenBlacklistSerializer(TokenBlacklistSerializer):
    token_class = SlidingToken
