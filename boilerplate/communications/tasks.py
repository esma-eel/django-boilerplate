from celery import shared_task
from django.conf import settings
from .utils.sms import kavenegar_send_sms


@shared_task
def kavenegar_celery_send_sms(
    receptor,
    template,
    token_data,
):
    try:
        response = kavenegar_send_sms(receptor, template, token_data)
        if response[0]["status"] in [4, 5]:
            return "sms sended"
        else:
            return response[0]["message"]
    except Exception as e:
        return "failed"
