import random
import string


def generate_from_chars(chars, length):
    result = "".join(random.choice(chars) for _ in range(length))
    return result


def generate_number(length):
    result = generate_from_chars(string.digits, length)
    return result


def generate_string_lc(length):
    result = generate_from_chars(string.ascii_lowercase, length)
    return result


def generate_string_uc(length):
    result = generate_from_chars(string.ascii_uppercase, length)
    return result
