from django.contrib.auth.models import AbstractUser
from common.models import BaseModel

from .managers import UserManager


class User(AbstractUser, BaseModel):
    """
    Default custom user model
    """

    #: First and last name do not cover name patterns around the globe
    first_name = None  # type: ignore
    last_name = None  # type: ignore
    email = None  # type: ignore
    EMAIL_FIELD = None
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []

    objects = UserManager()
