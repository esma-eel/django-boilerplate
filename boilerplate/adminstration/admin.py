from django.contrib import admin
from boilerplate.common.mixins import ModelAdminMixin
from .models import APIKey


@admin.register(APIKey)
class APIKeyModelAdmin(ModelAdminMixin):
    list_display = [
        "id",
        "name",
        "code",
        "description",
    ]

    search_fields = ["name", "code", "description"]
