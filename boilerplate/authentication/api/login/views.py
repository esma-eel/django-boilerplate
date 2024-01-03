from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from boilerplate.common.api.otp.serializers import (
    EmailAndOTPSerializer,
    PhoneNumberAndOTPSerializer,
)
from boilerplate.profiles.models import ProfileEmail, ProfilePhoneNumber

from .serializers import (
    EmailAndPasswordSerializer,
    PhoneNumberAndPasswordSerializer,
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

        phone_number = serializer.validated_data.get("phone_number")
        password = serializer.validated_data.get("password")

        qs_phone_numbers_objects = ProfilePhoneNumber.objects.filter(
            is_primary=True, number=phone_number, is_verified=True
        )

        if not qs_phone_numbers_objects.exists():
            return Response(
                {"phone_number": "Phone number is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

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

        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")

        qs_email_objects = ProfileEmail.objects.filter(
            is_primary=True, email=email, is_verified=True
        )

        if not qs_email_objects.exists():
            return Response(
                {"email": "Email is not valid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

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


class JWTCreateWithPhoneNumberAndOTPView(APIView):
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
            is_primary=True, number=phone_number, is_verified=True
        )
        if not qs_phone_numbers_objects.exists():
            return Response(
                {
                    "phone_number": (
                        "Please enter your verified primary phone number"
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        phone_number_object = qs_phone_numbers_objects.last()
        profile_user_obj = phone_number_object.profile.user

        headers = self.get_success_headers(request.data)

        jwt_refresh_obj = RefreshToken.for_user(profile_user_obj)
        return Response(
            {
                "refresh": str(jwt_refresh_obj),
                "access": str(jwt_refresh_obj.access_token),
            },
            status=status.HTTP_200_OK,
            headers=headers,
        )


class JWTCreateWithEmailAndOTPView(APIView):
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
        qs_email_objects = ProfileEmail.objects.filter(
            is_primary=True, email=email, is_verified=True
        )
        if not qs_email_objects.exists():
            return Response(
                {"email": "Please enter your verified primary email"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        email_object = qs_email_objects.last()
        profile_user_obj = email_object.profile.user

        headers = self.get_success_headers(request.data)

        jwt_refresh_obj = RefreshToken.for_user(profile_user_obj)
        return Response(
            {
                "refresh": str(jwt_refresh_obj),
                "access": str(jwt_refresh_obj.access_token),
            },
            status=status.HTTP_200_OK,
            headers=headers,
        )