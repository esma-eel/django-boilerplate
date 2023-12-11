from rest_framework import serializers
from boilerplate.common.utils.numbers import ir_phone_number
from rest_framework_simplejwt.tokens import RefreshToken, SlidingToken
from rest_framework_simplejwt.serializers import TokenBlacklistSerializer
from boilerplate.common.utils.redis_helpers import redis_get_key
from ..utils.otp_helpers import verify_input_otp_of_receiver


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)

    def validate_phone_number(self, value):
        if not ir_phone_number(value):
            raise serializers.ValidationError(
                {"phone_number": "Phone number is not valid"}
            )

        return value


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


class PhoneNumberAndOTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=11)
    otp = serializers.CharField()

    def validate_phone_number(self, value):
        if not ir_phone_number(value):
            raise serializers.ValidationError(
                {"phone_number": "Phone number is not valid"}
            )

        return value

    def validate_otp(self, value):
        if not value.isdigit():
            raise serializers.ValidationError(
                {"otp": "OTP Code format is wrong"}
            )

        return value

    def validate(self, attrs):
        phone_number = attrs.get("phone_number")
        otp = attrs.get("otp")

        result = verify_input_otp_of_receiver(phone_number, otp)

        if not result:
            raise serializers.ValidationError(
                {"otp": "OTP Code is wrong or expired"}
            )

        return attrs
