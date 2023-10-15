from django.contrib.auth.models import AbstractUser
from boilerplate.common import ModelMixin


class User(AbstractUser, ModelMixin):
    """
    Default custom user model
    """

    #: First and last name do not cover name patterns around the globe
    first_name = None  # type: ignore
    last_name = None  # type: ignore

    def get_absolute_url(self):
        pass
