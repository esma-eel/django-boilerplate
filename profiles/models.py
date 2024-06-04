from django.db import models
from common.mixins import ModelMixin
from django.utils.translation import gettext_lazy as _
from .utils.upload_path import profile_upload


class Profile(ModelMixin):
    name = models.CharField(_("Name"), max_length=32, blank=True, null=True)
    user = models.OneToOneField(
        "users.User", on_delete=models.PROTECT, verbose_name=_("User")
    )

    email = models.EmailField(_("Email"), unique=True)
    email_is_verified = models.BooleanField(default=False)

    phone_number = models.CharField(
        _("Phone Number"), max_length=11, unique=True,
    )
    phone_number_is_verified = models.BooleanField(default=False)

    city = models.CharField(_("City"), max_length=32, blank=True)
    address = models.TextField(_("Address"), blank=True)

    avatar = models.ImageField(
        _("Avatar"), blank=True, upload_to=profile_upload
    )

    def __str__(self):
        if self.name:
            return self.name

        return self.user.username
