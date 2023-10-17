from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken

from boilerplate.profiles.models import ProfilePhoneNumber, ProfileEmail
from .serializers import (
    PhoneNumberAndPasswordSerializer,
    EmailAndPasswordSerializer,
)


class JWTCreateWithPhoneNumberAndPassword(APIView):
    # authentication_classes = []
    # permission_classes = []

    allowed_methods = ["post"]
    http_method_names = ["post"]

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def post(self, request, *args, **kwargs):
        serializer = PhoneNumberAndPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.data.get("phone_number")
        password = serializer.data.get("password")

        qs_phone_numbers_objects = ProfilePhoneNumber.objects.filter(
            is_primary=True, number=phone_number, is_verified=True
        )

        if not qs_phone_numbers_objects.exists():
            raise ValidationError({"phone_number": "Phone number is not valid"})

        phone_number_object = qs_phone_numbers_objects.last()
        profile_user_obj = phone_number_object.profile.user
        authenticated_user = authenticate(
            username=profile_user_obj.username, password=password
        )

        headers = self.get_success_headers(request.data)

        if authenticated_user:
            jwt_refresh_obj = RefreshToken.for_user(authenticated_user)
            return Response(
                {
                    "refresh": str(jwt_refresh_obj),
                    "access": str(jwt_refresh_obj.access_token),
                },
                status=status.HTTP_200_OK,
                headers=headers,
            )

        return Response(
            {"message": "Phone number or password is wrong"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class JWTCreateWithEmailAndPassword(APIView):
    # authentication_classes = []
    # permission_classes = []

    allowed_methods = ["post"]
    http_method_names = ["post"]

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def post(self, request, *args, **kwargs):
        serializer = EmailAndPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data.get("email")
        password = serializer.data.get("password")

        qs_email_objects = ProfileEmail.objects.filter(
            is_primary=True, email=email, is_verified=True
        )

        if not qs_email_objects.exists():
            raise ValidationError({"email": "Email is not valid"})

        email_object = qs_email_objects.last()
        profile_user_obj = email_object.profile.user
        authenticated_user = authenticate(
            username=profile_user_obj.username, password=password
        )

        headers = self.get_success_headers(request.data)

        if authenticated_user:
            jwt_refresh_obj = RefreshToken.for_user(authenticated_user)
            return Response(
                {
                    "refresh": str(jwt_refresh_obj),
                    "access": str(jwt_refresh_obj.access_token),
                },
                status=status.HTTP_200_OK,
                headers=headers,
            )

        return Response(
            {"message": "Email or password is wrong"},
            status=status.HTTP_400_BAD_REQUEST,
        )
