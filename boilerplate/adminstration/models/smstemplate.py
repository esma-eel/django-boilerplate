from django.db import models
from boilerplate.common.mixins import ModelMixin


class SMSTemplate(ModelMixin):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=64, unique=True)
    description = models.TextField(null=True, blank=True)

    _tokens = models.TextField(
        help_text="Add values like: token, token10, ....", null=True, blank=True
    )

    def __str__(self):
        return f"{self.name} ({self.code})"

    @property
    def tokens(self):
        token_text = self._tokens
        token_list = token_text.split(", ")

        return token_list
