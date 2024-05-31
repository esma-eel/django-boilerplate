from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from common.api.otl.serializers import EmailAndOTLSerializer
from common.api.otl.mixins import RequestOTLApiMixin
from common.api.otp.serializers import PhoneOTPSerializer
from profiles.api.serializers import EmailReceiverSerializer, PhoneNumberReceiverSerializer
from .mixins import ChangePasswordApiMixin


class AuthenticatedUserChangePasswordApiView(ChangePasswordApiMixin, APIView):
    allowed_methods = ["post"]
    http_method_names = ["post"]
    permission_classes = [IsAuthenticated]


class ResetPasswordOTPWithPhoneNumberView(
    ChangePasswordApiMixin, APIView
):
    allowed_methods = ["post"]
    http_method_names = ["post"]
    receiver_serializer = PhoneNumberReceiverSerializer
    receiver_field = "phone_number"


class ResetPasswordRequestOTLWithEmailView(RequestOTLApiMixin, APIView):
    allowed_methods = ["post"]
    http_method_names = ["post"]
    receiver_serializer = EmailReceiverSerializer
    receiver_field = "email"
    profile_field = "email"

    def post(self, request, *args, **kwargs):
        serializer = self.receiver_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        receiver = serializer.validated_data.get(self.receiver_field)
        otl_sent = self.send_otl(receiver)

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
    ChangePasswordApiMixin, APIView
):
    allowed_methods = ["post"]
    http_method_names = ["post"]
    receiver_serializer = EmailReceiverSerializer
    receiver_field = "email"
