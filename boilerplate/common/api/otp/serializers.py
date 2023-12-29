from boilerplate.common.utils.number_helpers import ir_phone_number
from boilerplate.common.utils.otp_helpers import verify_input_otp_of_receiver
from rest_framework import serializers


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
