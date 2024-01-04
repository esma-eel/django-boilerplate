from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from boilerplate.common.api.otl.serializers import EmailAndOTLSerializer
from boilerplate.common.api.otl.views import RequestOTLApiMixin
from boilerplate.common.api.otp.serializers import PhoneOTPSerializer
from boilerplate.profiles.api.mixins import (
    ProfileEmailApiMixin,
    ProfilePhoneNumberApiMixin,
)
from .serializers import PasswordCheckSerializer


class ChangePasswordApiMixin:
    def get_password_serializer(self):
        return PasswordCheckSerializer

    def validate_password_serializer(self, request):
        password_serializer = self.get_password_serializer()
        self.password_serializer = password_serializer(data=request.data)
        self.password_serializer.is_valid(raise_exception=True)
        return self.password_serializer

    def get_password(self):
        return self.password_serializer.validated_data.get("password")

    def get_user(self, **kwargs):
        return self.request.user

    def change_password(self):
        user_obj = self.get_user()
        if user_obj:
            password_value = self.get_password()
            user_obj.set_password(password_value)
            user_obj.save()
            return True

        return False

    def post(self, request, *args, **kwargs):
        self.validate_password_serializer(request)
        is_changed = self.change_password()
        if is_changed:
            return Response(
                data={"message": "Password changed"},
                status=status.HTTP_200_OK,
            )

        return Response(
            data={"message": "Could'nt change password, try later"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class AuthenticatedUserChangePasswordApiView(ChangePasswordApiMixin, APIView):
    allowed_methods = ["post"]
    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]


class ResetPasswordOTPWithPhoneNumberView(
    ChangePasswordApiMixin, ProfilePhoneNumberApiMixin, APIView
):
    allowed_methods = ["post"]
    http_method_names = ["post"]

    def get_profile_serializer(self):
        return PhoneOTPSerializer

    def get_profile_serializer_field_name(self):
        return "receiver"

    def get_user(self, **kwargs):
        return self.get_profile_user()

    def post(self, request, *args, **kwargs):
        self.validate_password_serializer(request)
        self.validate_profile_serializer(request)
        is_changed = self.change_password()
        if is_changed:
            return Response(
                data={"message": "Password reset completed"},
                status=status.HTTP_200_OK,
            )

        return Response(
            data={"message": "Could'nt reset password, try later"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ResetPasswordRequestOTLWithEmailView(RequestOTLApiMixin, APIView):
    allowed_methods = ["post"]
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        self.validate_receiver_serializer(request)
        otl_sent = self.send_otl()

        if not otl_sent:
            return Response(
                data={"message": "OTL Service is down, try later"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response(
            data={"message": "OTL Sent!"},
            status=status.HTTP_200_OK,
        )


class ResetPasswordOTLWithEmailView(
    ChangePasswordApiMixin, ProfileEmailApiMixin, APIView
):
    allowed_methods = ["post"]
    http_method_names = ["post"]

    def get_profile_serializer(self):
        return EmailAndOTLSerializer

    def get_profile_serializer_field_name(self):
        return "email"

    def get_user(self, **kwargs):
        return self.get_profile_user()

    def post(self, request, *args, **kwargs):
        self.validate_password_serializer(request)
        self.validate_profile_serializer(request)
        is_changed = self.change_password()
        if is_changed:
            return Response(
                data={"message": "Password reset completed"},
                status=status.HTTP_200_OK,
            )

        return Response(
            data={"message": "Could'nt reset password, try later"},
            status=status.HTTP_400_BAD_REQUEST,
        )
