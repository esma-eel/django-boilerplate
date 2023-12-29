from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from boilerplate.common.api.otp.serializers import (
    EmailAndOTPSerializer, PhoneNumberAndOTPSerializer)
from boilerplate.profiles.models import ProfileEmail, ProfilePhoneNumber


class VerifyPhoneNumberWithOTPView(APIView):
    allowed_methods = ["post"]
    http_method_names = ["post"]

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def post(self, request, *args, **kwargs):
        serializer = PhoneNumberAndOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data.get("phone_number")
        qs_phone_numbers_objects = ProfilePhoneNumber.objects.filter(
            number=phone_number
        )
        if not qs_phone_numbers_objects.exists():
            return Response(
                {"phone_number": "Phone number does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        phone_number_object = qs_phone_numbers_objects.last()

        if phone_number_object.is_verified:
            return Response(
                {"phone_number": "Phone number is already verified"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        phone_number_object.is_verified = True
        phone_number_object.save()

        headers = self.get_success_headers(request.data)

        return Response(
            {"message": "Phone number verified successfully"},
            status=status.HTTP_200_OK,
            headers=headers,
        )


class VerifyEmailWithOTPView(APIView):
    allowed_methods = ["post"]
    http_method_names = ["post"]

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def post(self, request, *args, **kwargs):
        serializer = EmailAndOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")
        qs_email_objects = ProfileEmail.objects.filter(email=email)
        if not qs_email_objects.exists():
            return Response(
                {"phone_number": "Email does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        email_object = qs_email_objects.last()

        if email_object.is_verified:
            return Response(
                {"phone_number": "Email is already verified"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        email_object.is_verified = True
        email_object.save()

        headers = self.get_success_headers(request.data)

        return Response(
            {"message": "Email verified successfully"},
            status=status.HTTP_200_OK,
            headers=headers,
        )
