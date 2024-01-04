from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.views import APIView

from boilerplate.profiles.api.serializers import (
    EmailSerializer,
    PhoneNumberSerializer,
)
from boilerplate.common.utils.otp_helpers import (
    generate_otp_for_receiver,
    send_otp_to_receiver_sms,
    send_otp_to_receiver_email,
)

from .serializers import EmailOTPSerializer, PhoneOTPSerializer


class RequestOTPApiMixin(APIView):
    allowed_methods = ["post"]
    http_method_names = ["post"]
    serializer = None
    receiver_field = ""

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def generate_otp(self):
        receiver = self.get_receiver()
        return generate_otp_for_receiver(receiver)

    def get_receiver(self):
        return self.receiver_serialzier.validated_data.get(self.receiver_field)

    def get_communication_function(self):
        return None

    def send_otp(self):
        otp_value = self.generate_otp()
        receiver = self.get_receiver()
        communication_function = self.get_communication_function()

        if otp_value:
            result = communication_function(receiver, otp_value)
            return result

        return False

    def post(self, request, *args, **kwargs):
        self.receiver_serialzier = self.serializer(data=request.data)
        self.receiver_serialzier.is_valid(raise_exception=True)
        receiver = self.get_receiver()
        otp_sent = self.send_otp()
        headers = self.get_success_headers(request.data)

        if not otp_sent:
            return Response(
                data={"message": "OTP Service is down, try later"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response(
            data={"message": f"OTP Sent to {receiver}"},
            status=status.HTTP_200_OK,
            headers=headers,
        )


class VerifyOTPApiView(APIView):
    allowed_methods = ["post"]
    http_method_names = ["post"]
    serializer = None

    def get_success_headers(self, data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def post(self, request, *args, **kwargs):
        serializer = self.serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(request.data)
        return Response(
            data={"message": "OK!"},
            status=status.HTTP_200_OK,
            headers=headers,
        )


class RequestOTPPhoneApiView(RequestOTPApiMixin):
    serializer = PhoneNumberSerializer
    receiver_field = "phone_number"

    def get_communication_function(self):
        return send_otp_to_receiver_sms


class RequestOTPEmailApiView(RequestOTPApiMixin):
    serializer = EmailSerializer
    receiver_field = "email"

    def get_communication_function(self):
        return send_otp_to_receiver_email


class VerifyOTPPhoneApiView(VerifyOTPApiView):
    serializer = PhoneOTPSerializer


class VerifyOTPEmailApiView(VerifyOTPApiView):
    serializer = EmailOTPSerializer
