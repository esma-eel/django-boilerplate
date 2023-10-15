from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class ProfilesConfig(AppConfig):
    name = "boilerplate.profiles"
    verbose_name = _("Profiles")

    def ready(self):
        pass
        # import boilerplate.profiles.signals
