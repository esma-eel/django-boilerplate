from rest_framework.views import APIView

from boilerplate.common.api.otp.serializers import (
    EmailOTPSerializer,
    PhoneOTPSerializer,
)
from .mixins import (
    ProfilePhoneNumberApiMixin,
    ProfileEmailApiMixin,
    ProfileFieldVerifyApiMixin,
)


class VerifyPhoneNumberWithOTPView(
    ProfileFieldVerifyApiMixin,
    ProfilePhoneNumberApiMixin,
    APIView,
):
    allowed_methods = ["post"]
    http_method_names = ["post"]

    def get_profile_serializer(self):
        return PhoneOTPSerializer

    def get_profile_serializer_field_name(self):
        return "receiver"


class VerifyEmailWithOTPView(
    ProfileFieldVerifyApiMixin,
    ProfileEmailApiMixin,
    APIView,
):
    allowed_methods = ["post"]
    http_method_names = ["post"]

    def get_profile_serializer(self):
        return EmailOTPSerializer

    def get_profile_serializer_field_name(self):
        return "receiver"
