from django.db import models
from boilerplate.common.mixins import ModelMixin


class EmailTemplate(ModelMixin):
    name = models.CharField(max_length=64)
    code = models.CharField(max_length=64, unique=True)
    content = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.code})"
