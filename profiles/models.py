from django.db import models
from common.models import BaseModel
from django.utils.translation import gettext_lazy as _
from .managers import ProfileManager


class Profile(BaseModel):
    user = models.OneToOneField(
        "users.User", on_delete=models.PROTECT, verbose_name=_("User")
    )
    name = models.CharField(_("Name"), max_length=32, blank=True, null=True)
    email = models.EmailField(_("Email"), null=True, blank=True)

    objects = ProfileManager()

    def __str__(self):
        if self.name:
            return self.name

        return self.user.username
