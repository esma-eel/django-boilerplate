from rest_framework.views import APIView

from common.api.otp.serializers import (
    EmailOTPSerializer,
    PhoneOTPSerializer,
)
from .serializers import (
    EmailPasswordSerializer,
    PhonePasswordSerializer,
)
from .mixins import (
    JWTCreateProfilePasswordApiMixin,
    JWTCreateProfileFieldOTPApiMixin,
)


class JWTCreatePhonePasswordApiView(JWTCreateProfilePasswordApiMixin, APIView):
    allowed_methods = ["post"]
    http_method_names = ["post"]
    serializer = PhonePasswordSerializer
    receiver_field = "phone_number"
    profile_field = "phone_number"


class JWTCreateEmailPasswordApiView(JWTCreateProfilePasswordApiMixin, APIView):
    allowed_methods = ["post"]
    http_method_names = ["post"]
    serializer = EmailPasswordSerializer
    receiver_field = "email"
    profile_field = "email"


class JWTCreatePhoneOTPApiView(JWTCreateProfileFieldOTPApiMixin, APIView):
    allowed_methods = ["post"]
    http_method_names = ["post"]
    serializer = PhoneOTPSerializer
    receiver_field = "receiver"
    profile_field = "phone_number"


class JWTCreateEmailOTPApiView(JWTCreateProfileFieldOTPApiMixin, APIView):
    allowed_methods = ["post"]
    http_method_names = ["post"]
    serializer = EmailOTPSerializer
    receiver_field = "receiver"
    profile_field = "email"
