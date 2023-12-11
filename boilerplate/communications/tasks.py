from celery import shared_task
from django.conf import settings
from .utils.sms import send_sms


@shared_task
def celery_sms(
    receptor,
    template,
    token_data,
):
    try:
        response = send_sms(receptor, template, token_data)
        if response[0]["status"] in [4, 5]:
            return "sms sended"
        else:
            return response[0]["message"]
    except Exception as e:
        return "failed"
