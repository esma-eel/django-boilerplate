from rest_framework.reverse import reverse
from common.utils.otl_helpers import (
    generate_otl_for_receiver,
    send_otl_to_receiver_email,
)


class RequestOTLApiMixin:
    receiver_serializer = None
    receiver_field = ""

    def generate_otl(self, receiver):
        return generate_otl_for_receiver(receiver)

    def get_communication_function(self):
        return send_otl_to_receiver_email

    def send_otl(self, receiver):
        otl_value = self.generate_otl(receiver)
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
