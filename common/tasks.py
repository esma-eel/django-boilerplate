from celery import shared_task
from .utils.email import send_email


@shared_task
def celery_send_email(
    json_content,
    to_emails,
):
    try:
        response = send_email(
            to_emails,
            json_content,
        )
        if response == 1:
            return True
        else:
            return False
    except Exception:
        return False
