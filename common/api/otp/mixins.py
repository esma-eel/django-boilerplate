from rest_framework import status
from rest_framework.response import Response

from common.utils.otp_helpers import generate_otp_for_receiver


class RequestOTPApiMixin:
    receiver_serializer = None
    receiver_field = ""

    def generate_otp(self, receiver):
        return generate_otp_for_receiver(receiver)

    def get_communication_function(self):
        return None

    def send_otp(self, receiver):
        otp_value = self.generate_otp(receiver)
        communication_function = self.get_communication_function()

        if otp_value:
            result = communication_function(receiver, otp_value)
            return result

        return False

    def post(self, request, *args, **kwargs):
        serializer = self.receiver_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        receiver = serializer.validated_data.get(self.receiver_field)
        otp_sent = self.send_otp(receiver)

        if not otp_sent:
            return Response(
                data={"message": "OTP Service is down, try later"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response(
            data={"message": "OTP Sent"},
            status=status.HTTP_200_OK,
        )


class VerifyOTPApiMixin:
    receiver_serializer = None

    def post(self, request, *args, **kwargs):
        serializer = self.receiver_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return Response(
            data={"message": "OK!"},
            status=status.HTTP_200_OK,
        )
