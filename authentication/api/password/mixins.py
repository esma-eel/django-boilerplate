from rest_framework import status
from rest_framework.response import Response
from profiles.models import Profile
from .serializers import PasswordCheckSerializer


class ChangePasswordApiMixin:
    password_serializer = PasswordCheckSerializer

    def change_password(self, user, password):
        if user:
            user.set_password(password)
            user.save()
            return True

        return False

    def post(self, request, *args, **kwargs):
        password_serializer = self.password_serializer(data=request.data)
        password_serializer.is_valid(raise_exception=True)
        user = request.user
        password = password_serializer.validated_data.get("password")
        is_changed = self.change_password(user, password)

        if is_changed:
            return Response(
                data={"message": "Password changed"},
                status=status.HTTP_200_OK,
            )

        return Response(
            data={"message": "Could'nt change password, try later"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ChangePasswordAPIMixinWithProfileField(ChangePasswordApiMixin):
    password_serializer = PasswordCheckSerializer
    receiver_serializer = None
    receiver_field = ""

    def change_password(self, user, password):
        if user:
            user.set_password(password)
            user.save()
            return True

        return False

    def post(self, request, *args, **kwargs):
        password_serializer = self.password_serializer(data=request.data)
        password_serializer.is_valid(raise_exception=True)

        receiver_serializer = self.receiver_serializer(data=request.data)
        receiver_serializer.is_valid(raise_exception=True)
        receiver = receiver_serializer.validated_data.get(self.receiver_field)
        qs = Profile.objects.filter(**{self.receiver_field: receiver})
        if not qs.exists():
            return Response(
                data={"message": "Wrong receiver!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        user = qs.last().user
        password = password_serializer.validated_data.get("password")
        is_changed = self.change_password(user, password)

        if is_changed:
            return Response(
                data={"message": "Password changed"},
                status=status.HTTP_200_OK,
            )

        return Response(
            data={"message": "Could'nt change password, try later"},
            status=status.HTTP_400_BAD_REQUEST,
        )