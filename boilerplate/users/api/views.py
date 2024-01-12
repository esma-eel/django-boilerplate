import copy
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.db import transaction
from .serializers import CreateUserModelSerializer, UserModelSerializer

User = get_user_model()


class UserCreateAPIView(APIView):
    serializer_class = CreateUserModelSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def profile_update(self, user_object, profile_data):
        profile_object = user_object.profile
        phone_numbers_data = profile_data.pop("phone_numbers")
        emails_data = profile_data.pop("emails")
        addresses_data = profile_data.pop("addresses")

        for attr, value in profile_data.items():
            setattr(profile_object, attr, value)
        profile_object.save()

        for phone_number_data in phone_numbers_data:
            profile_object.phone_number_set.create(**phone_number_data)

        for email_data in emails_data:
            profile_object.email_set.create(**email_data)

        for address_data in addresses_data:
            profile_object.address_set.create(**address_data)

        profile_object.save()
        return profile_object

    def authentication_set(self, user_object, authenticate_data):
        password = authenticate_data.get("password")
        user_object.set_password(password)
        user_object.save()
        return user_object

    def user_create(self, user_data):
        profile_data = user_data.pop("profile")
        user_object = User.objects.create(**user_data)
        self.profile_update(user_object, profile_data)
        return user_object

    @transaction.atomic()
    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer_data = copy.deepcopy(serializer.data)
        user_data = serializer_data.pop("user")
        authentication_data = serializer_data.pop("authentication")

        user_object = self.user_create(user_data)
        self.authentication_set(user_object, authentication_data)

        created_serializer = UserModelSerializer(instance=user_object)

        return Response(
            created_serializer.data,
            status=status.HTTP_201_CREATED,
        )
