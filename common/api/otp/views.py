from rest_framework.views import APIView

from common.utils.otp_helpers import (
    send_otp_to_receiver_sms,
    send_otp_to_receiver_email,
)
from profiles.api.serializers import (
    PhoneNumberReceiverSerializer,
    EmailReceiverSerializer,
)
from .serializers import EmailOTPSerializer, PhoneOTPSerializer
from .mixins import VerifyOTPApiMixin, RequestOTPApiMixin


class RequestOTPPhoneApiView(RequestOTPApiMixin, APIView):
    allowed_methods = ["post"]
    http_method_names = ["post"]
    receiver_serializer = PhoneNumberReceiverSerializer
    receiver_field = "phone_number"

    def get_communication_function(self):
        return send_otp_to_receiver_sms


class RequestOTPEmailApiView(RequestOTPApiMixin, APIView):
    allowed_methods = ["post"]
    http_method_names = ["post"]
    receiver_serializer = EmailReceiverSerializer
    receiver_field = "email"

    def get_communication_function(self):
        return send_otp_to_receiver_email


class VerifyOTPPhoneApiView(VerifyOTPApiMixin, APIView):
    allowed_methods = ["post"]
    http_method_names = ["post"]
    receiver_serializer = PhoneOTPSerializer


class VerifyOTPEmailApiView(VerifyOTPApiMixin, APIView):
    allowed_methods = ["post"]
    http_method_names = ["post"]
    receiver_serializer = EmailOTPSerializer
