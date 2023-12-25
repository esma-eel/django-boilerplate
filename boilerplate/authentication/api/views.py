from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenBlacklistView

from boilerplate.profiles.models import ProfilePhoneNumber, ProfileEmail
from .serializers import (
    PhoneNumberAndPasswordSerializer,
    EmailAndPasswordSerializer,
    PhoneNumberSerializer,
    PhoneNumberAndOTPSerializer,
    EmailSerializer,
    EmailAndOTPSerializer,
    PasswordCheckSerializer,
)

from ..utils.otp_helpers import generate_otp_for_receiver
from boilerplate.communications.tasks import (
    kavenegar_celery_send_sms,
    celery_send_email,
)
from boilerplate.adminstration.models import SMSTemplate, EmailTemplate


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


class JWTTokenBlacklistView(TokenBlacklistView):
    _serializer_class = (
        "boilerplate.authentication.api.serializers.JWTTokenBlacklistSerializer"
    )


class SlidingTokenBlacklistView(TokenBlacklistView):
    _serializer_class = (
        "boilerplate.authentication.api.serializers"
        ".SlidingTokenBlacklistSerializer"
    )


# otp phone number
class RequestOTPWithPhoneNumberView(APIView):
    allowed_methods = ["post"]
    http_method_names = ["post"]

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def post(self, request, *args, **kwargs):
        serializer = PhoneNumberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data.get("phone_number")

        otp_value = generate_otp_for_receiver(phone_number)

        if otp_value:
            headers = self.get_success_headers(request.data)
            try:
                token_data = {"token": otp_value}
                sms_template = SMSTemplate.objects.get(code="otp1")
                kavenegar_celery_send_sms.delay(
                    receptor=phone_number,
                    template=sms_template.code,
                    token_data=token_data,
                )

                return Response(
                    data={"message": f"OTP Sent to {phone_number}"},
                    status=status.HTTP_200_OK,
                    headers=headers,
                )
            except Exception:
                return Response(
                    data={"message": "There is no sms template for otp"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(
            data={"message": "Cant create otp, try later"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class VerifyOTPWithPhoneNumberView(APIView):
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
        headers = self.get_success_headers(request.data)
        return Response(
            data={"message": "OTP is right"},
            status=status.HTTP_200_OK,
            headers=headers,
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


# otp email
class RequestOTPWithEmailView(APIView):
    allowed_methods = ["post"]
    http_method_names = ["post"]

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def post(self, request, *args, **kwargs):
        serializer = EmailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data.get("email")

        otp_value = generate_otp_for_receiver(email)

        if otp_value:
            headers = self.get_success_headers(request.data)
            try:
                token_data = {"token": otp_value}
                email_template = EmailTemplate.objects.get(code="otp1")
                email_content = email_template.content.format(**token_data)
                json_content = {
                    "title": email_template.name,
                    "content": email_content,
                }
                to_emails = [email]
                celery_send_email.delay(json_content, to_emails)

                return Response(
                    data={"message": f"OTP Sent to {email}"},
                    status=status.HTTP_200_OK,
                    headers=headers,
                )
            except Exception:
                return Response(
                    data={"message": "There is no email template for otp"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(
            data={"message": "Cant create otp, try later"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class VerifyOTPWithEmailView(APIView):
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
        headers = self.get_success_headers(request.data)
        return Response(
            data={"message": "OTP is right"},
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


class ResetPasswordOTPWithPhoneNumberView(APIView):
    allowed_methods = ["post"]
    http_method_names = ["post"]

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def post(self, request, *args, **kwargs):
        password_serializer = PasswordCheckSerializer(data=request.data)
        password_serializer.is_valid(raise_exception=True)
        phone_number_otp_serializer = PhoneNumberAndOTPSerializer(
            data=request.data
        )
        phone_number_otp_serializer.is_valid(raise_exception=True)

        phone_number = phone_number_otp_serializer.validated_data.get(
            "phone_number"
        )

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

        password_value = password_serializer.validated_data.get("password")
        profile_user_obj.set_password(password_value)
        profile_user_obj.save()

        headers = self.get_success_headers(request.data)
        return Response(
            data={
                "message": (
                    f"Password reset for user '{profile_user_obj}' was"
                    " successful"
                )
            },
            status=status.HTTP_200_OK,
            headers=headers,
        )
