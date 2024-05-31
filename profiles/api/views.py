from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from common.api.otp.mixins import VerifyOTPApiMixin
from common.api.otp.serializers import (
    EmailOTPSerializer,
    PhoneOTPSerializer,
)
from .serializers import (
    ProfileModelSerializer,
)
from profiles.models import Profile


class VerifyPhoneNumberWithOTPView(
    VerifyOTPApiMixin,
    APIView,
):
    allowed_methods = ["post"]
    http_method_names = ["post"]
    receiver_serializer = PhoneOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.receiver_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get("receiver")

        qs = Profile.objects.filter(phone_number=phone_number)
        if not qs.exists():
            return Response(
                data={"message": "Wrong Receiver!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        profile = qs.last()
        profile.phone_number_is_verified = True
        profile.save()

        return Response(
            data={"message": "OK!"},
            status=status.HTTP_200_OK,
        )


class VerifyEmailWithOTPView(
    VerifyOTPApiMixin,
    APIView,
):
    allowed_methods = ["post"]
    http_method_names = ["post"]
    receiver_serializer = EmailOTPSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.receiver_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("receiver")

        qs = Profile.objects.filter(email=email)
        if not qs.exists():
            return Response(
                data={"message": "Wrong Receiver!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        profile = qs.last()
        profile.email_is_verified = True
        profile.save()

        return Response(
            data={"message": "OK!"},
            status=status.HTTP_200_OK,
        )


class RetrieveUpdateProfileAPIView(RetrieveUpdateAPIView):
    allowed_methods = ["get", "patch"]
    http_method_names = ["get", "patch"]

    permission_classes = []

    serializer_class = ProfileModelSerializer
    lookup_field = "user__username"

    queryset = Profile.objects.all()
