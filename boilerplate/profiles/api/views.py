from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from boilerplate.common.api.otp.serializers import (
    EmailOTPSerializer,
    PhoneOTPSerializer,
)
from boilerplate.profiles.models import ProfileEmail, ProfilePhoneNumber


class ProfileFieldVerificationAPIView(APIView):
    serializer = None
    field = None
    model = None
    model_field = None

    allowed_methods = ["post"]
    http_method_names = ["post"]

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def post(self, request, *args, **kwargs):
        serializer = self.serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        field_value = serializer.validated_data.get(self.field)
        queryset = self.model.objects.filter(**{self.model_field: field_value})
        if not queryset.exists():
            return Response(
                {self.field: "does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        object = queryset.last()

        if object.is_verified:
            return Response(
                {self.field: "already verified"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        object.is_verified = True
        object.save()

        headers = self.get_success_headers(request.data)

        return Response(
            {"message": "verified successfully"},
            status=status.HTTP_200_OK,
            headers=headers,
        )


class VerifyPhoneNumberWithOTPView(ProfileFieldVerificationAPIView):
    serializer = PhoneOTPSerializer
    field = "phone_number"
    model = ProfilePhoneNumber
    model_field = "number"


class VerifyEmailWithOTPView(ProfileFieldVerificationAPIView):
    serializer = EmailOTPSerializer
    field = "email"
    model = ProfileEmail
    model_field = "email"

