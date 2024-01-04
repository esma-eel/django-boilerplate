from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from boilerplate.common.api.otp.serializers import (
    EmailOTPSerializer,
    PhoneOTPSerializer,
)
from boilerplate.profiles.api.mixins import (
    ProfileFieldApiMixin,
    ProfilePhoneNumberApiMixin,
    ProfileEmailApiMixin,
)
from .serializers import (
    EmailPasswordSerializer,
    PhonePasswordSerializer,
)


class JWTCreateProfilePasswordApiMixin(ProfileFieldApiMixin):
    def get_password(self):  # -> Any:
        return self.profile_serializer.validated_data.get("password")

    def authenticate_user(self):
        password = self.get_password()
        user = self.get_profile_user()

        if user and password:
            authenticated_user = authenticate(
                username=user.username, password=password
            )
            return authenticated_user

        return None

    def get_tokens(self):
        authenticated_user = self.authenticate_user()
        if authenticated_user:
            jwt_refresh_obj = RefreshToken.for_user(authenticated_user)
            return {
                "refresh": str(jwt_refresh_obj),
                "access": str(jwt_refresh_obj.access_token),
            }

        return {}

    def post(self, request, *args, **kwargs):
        self.validate_profile_serializer(request)
        tokens = self.get_tokens()
        if tokens:
            return Response(tokens, status=status.HTTP_200_OK)

        return Response(
            {"message": "User not found or Password is wrong"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class JWTCreateProfileFieldOTPApiMixin(JWTCreateProfilePasswordApiMixin):
    def get_tokens(self):
        authenticated_user = self.get_profile_user()
        if authenticated_user:
            jwt_refresh_obj = RefreshToken.for_user(authenticated_user)
            return {
                "refresh": str(jwt_refresh_obj),
                "access": str(jwt_refresh_obj.access_token),
            }

        return {}


class JWTCreatePhonePasswordApiView(
    JWTCreateProfilePasswordApiMixin, ProfilePhoneNumberApiMixin, APIView
):
    allowed_methods = ["post"]
    http_method_names = ["post"]

    def get_profile_serializer(self):
        return PhonePasswordSerializer


class JWTCreateEmailPasswordApiView(
    JWTCreateProfilePasswordApiMixin, ProfileEmailApiMixin, APIView
):
    allowed_methods = ["post"]
    http_method_names = ["post"]

    def get_profile_serializer(self):
        return EmailPasswordSerializer


class JWTCreatePhoneOTPApiView(
    JWTCreateProfileFieldOTPApiMixin, ProfilePhoneNumberApiMixin, APIView
):
    allowed_methods = ["post"]
    http_method_names = ["post"]

    def get_profile_serializer(self):
        return PhoneOTPSerializer

    def get_profile_serializer_field_name(self):
        return "receiver"


class JWTCreateEmailOTPApiView(
    JWTCreateProfileFieldOTPApiMixin, ProfileEmailApiMixin, APIView
):
    allowed_methods = ["post"]
    http_method_names = ["post"]

    def get_profile_serializer(self):
        return EmailOTPSerializer

    def get_profile_serializer_field_name(self):
        return "receiver"
