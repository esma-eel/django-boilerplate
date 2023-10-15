from django.db import models
from boilerplate.common import ModelMixin
from django.utils.translation import gettext_lazy as _
import uuid
from .utils.upload_path import profile_upload


class Profile(ModelMixin):
    uuid = models.UUIDField(
        _("UUID"), unique=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(_("Name"), max_length=32, blank=True, null=True)
    avatar = models.ImageField(
        _("Avatar"), blank=True, null=True, upload_to=profile_upload
    )

    user = models.OneToOneField(
        "users.User", on_delete=models.PROTECT, verbose_name=_("User")
    )

    def __str__(self):
        return self.name


class ProfileEmail(ModelMixin):
    email = models.EmailField(_("Email"), unique=True)
    is_primary = models.BooleanField(default=False)

    profile = models.ForeignKey(
        "profiles.Profile", on_delete=models.CASCADE, related_name="email_set"
    )

    def __str__(self):
        return self.email


class ProfilePhoneNumber(ModelMixin):
    number = models.CharField(_("Number"), max_length=11, unique=True)
    is_primary = models.BooleanField(default=False)

    profile = models.ForeignKey(
        "profiles.Profile",
        on_delete=models.CASCADE,
        related_name="phone_number_set",
    )

    def __str__(self):
        return self.number


class ProfileAddress(ModelMixin):
    city = models.CharField(_("City"), max_length=32, blank=True, null=True)
    address = models.TextField(_("Address"))

    profile = models.ForeignKey(
        "profiles.Profile",
        on_delete=models.CASCADE,
        related_name="address_set",
    )

    def __str__(self):
        return f"{self.profile} Address"
