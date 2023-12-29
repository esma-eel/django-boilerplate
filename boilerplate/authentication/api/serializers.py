import re
from rest_framework import serializers
from boilerplate.common.utils.numbers import ir_phone_number
from rest_framework_simplejwt.tokens import RefreshToken, SlidingToken
from rest_framework_simplejwt.serializers import TokenBlacklistSerializer
from ..utils.otp_helpers import verify_input_otp_of_receiver
from ..utils.otl_helpers import verify_input_otl_of_receiver


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


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class EmailAndOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

    def validate_otp(self, value):
        if not value.isdigit():
            raise serializers.ValidationError(
                {"otp": "OTP Code format is wrong"}
            )

        return value

    def validate(self, attrs):
        email = attrs.get("email")
        otp = attrs.get("otp")

        result = verify_input_otp_of_receiver(email, otp)

        if not result:
            raise serializers.ValidationError(
                {"otp": "OTP Code is wrong or expired"}
            )

        return attrs


class PasswordCheckSerializer(serializers.Serializer):
    password = serializers.CharField()
    repeat_password = serializers.CharField()

    def validate_password(self, value):
        password_pattern = (
            r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        )
        if not re.match(password_pattern, value):
            raise serializers.ValidationError(
                {
                    "password": [
                        "At least minimum 8 characters in length",
                        "At least one uppercase English letter",
                        "At least one lowercase English letter",
                        "At least one digit",
                        "At least one special character [#?!@$%^&*-]",
                    ]
                }
            )
        return value

    def validate(self, attrs):
        password = attrs.get("password")
        repeat_password = attrs.get("repeat_password")

        if password != repeat_password:
            raise serializers.ValidationError(
                {
                    "message": (
                        "password and repeat password values, are not equal"
                    )
                }
            )

        return attrs


class EmailAndOTLSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otl = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        otl = attrs.get("otl")

        result = verify_input_otl_of_receiver(otl, email)

        if not result:
            raise serializers.ValidationError(
                {"otl": "OTL Token is wrong or expired"}
            )

        return attrs
