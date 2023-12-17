from boilerplate.common.utils.redis_helpers import (
    redis_set_kvt,
    redis_get_key,
    redis_remove_key,
)
from boilerplate.common.utils.generators import generate_number


def get_otp_key(receiver):
    key = f"{receiver}_otp"
    return key


def generate_otp_for_receiver(receiver):
    otp = generate_number(5)
    lifetime = 300  # seconds
    receiver_key = get_otp_key(receiver)
    otp_is_created = redis_set_kvt(receiver_key, otp, lifetime)
    if otp_is_created:
        return get_otp_of_receiver(receiver)

    return None


def get_otp_of_receiver(receiver):
    receiver_key = get_otp_key(receiver)
    otp_value = redis_get_key(receiver_key)
    return otp_value


def expire_otp(receiver):
    receiver_key = get_otp_key(receiver)
    expire_result = redis_remove_key(receiver_key)
    return expire_result


def verify_input_otp_of_receiver(receiver, input_otp):
    receiver_otp = get_otp_of_receiver(receiver)
    if receiver_otp and receiver_otp == input_otp:
        is_expired = expire_otp(receiver)
        return is_expired

    return None
