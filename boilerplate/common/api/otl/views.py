from rest_framework.reverse import reverse
from boilerplate.common.utils.otl_helpers import (
    generate_otl_for_receiver,
    send_otl_to_receiver_email,
)
from boilerplate.profiles.api.serializers import EmailSerializer


class RequestOTLApiMixin:
    def get_receiver_serializer(self):
        return EmailSerializer

    def get_receiver_serializer_field(self):
        return "email"

    def validate_receiver_serializer(self, request):
        serializer = self.get_receiver_serializer()
        self.receiver_serialzier = serializer(data=request.data)
        self.receiver_serialzier.is_valid(raise_exception=True)
        return self.receiver_serialzier

    def generate_otl(self):
        receiver = self.get_receiver()
        return generate_otl_for_receiver(receiver)

    def get_receiver(self):
        receiver_field_name = self.get_receiver_serializer_field()
        return self.receiver_serialzier.validated_data.get(receiver_field_name)

    def get_communication_function(self):
        return send_otl_to_receiver_email

    def send_otl(self):
        otl_value = self.generate_otl()
        receiver = self.get_receiver()
        communication_function = self.get_communication_function()

        if otl_value:
            link = reverse(
                "api-authentication:reset-password-email-otl",
                args=[otl_value],
                request=self.request,
            )
            result = communication_function(receiver, link)
            return result

        return False
