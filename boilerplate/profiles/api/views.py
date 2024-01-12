from django.db import transaction
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveUpdateAPIView
from boilerplate.common.api.otp.serializers import (
    EmailOTPSerializer,
    PhoneOTPSerializer,
)
from .mixins import (
    ProfilePhoneNumberApiMixin,
    ProfileEmailApiMixin,
    ProfileFieldVerifyApiMixin,
)

from .serializers import (
    ProfileModelSerializer,
)
from boilerplate.profiles.models import Profile


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


class RetrieveUpdateProfileAPIView(RetrieveUpdateAPIView):
    allowed_methods = ["get", "patch"]
    http_method_names = ["get", "patch"]

    permission_classes = []

    serializer_class = ProfileModelSerializer
    lookup_field = "user__username"

    queryset = Profile.objects.all()

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    @transaction.atomic()
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()

        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )

        serializer.is_valid(raise_exception=True)

        serializer.validated_data.pop("phone_number_set", None)
        serializer.validated_data.pop("email_set", None)
        serializer.validated_data.pop("address_set", None)

        phone_numbers = request.data.get("phone_numbers", [])
        emails = request.data.get("emails", [])
        addresses = request.data.get("addresses", [])

        extra_data = {
            "phone_numbers": phone_numbers,
            "emails": emails,
            "addresses": addresses,
        }
        self.perform_update(serializer, extra_data)  # update profile instance

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer, extra_data):
        updated_object = serializer.save()

        phone_numbers = extra_data.pop("phone_numbers")
        emails = extra_data.pop("emails")
        addresses = extra_data.pop("addresses")

        for phone_number in phone_numbers:
            id = phone_number.pop("id", None)
            if id:
                qs = updated_object.phone_number_set.filter(id=id)
                if qs.exists():
                    sub_object = qs.last()
                    for attr, value in phone_number.items():
                        setattr(sub_object, attr, value)
                    sub_object.save()
            else:
                updated_object.phone_number_set.create(**phone_number)

        for email in emails:
            id = email.pop("id", None)
            if id:
                qs = updated_object.email_set.filter(id=id)
                if qs.exists():
                    sub_object = qs.last()
                    for attr, value in email.items():
                        setattr(sub_object, attr, value)
                    sub_object.save()
            else:
                updated_object.email_set.create(**email)

        for address in addresses:
            id = address.pop("id", None)
            if id:
                qs = updated_object.address_set.filter(id=id)
                if qs.exists():
                    sub_object = qs.last()
                    for attr, value in address.items():
                        setattr(sub_object, attr, value)
                    sub_object.save()
            else:
                updated_object.address_set.create(**address)

        updated_object.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)
