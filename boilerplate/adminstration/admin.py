from django.contrib import admin
from boilerplate.common.mixins import ModelAdminMixin
from .models import APIKey, SMSTemplate, EmailTemplate


@admin.register(APIKey)
class APIKeyModelAdmin(ModelAdminMixin):
    list_display = [
        "id",
        "name",
        "code",
        "description",
    ]

    search_fields = ["name", "code", "description"]


@admin.register(SMSTemplate)
class SMSTemplateModelAdmin(ModelAdminMixin):
    list_display = [
        "id",
        "name",
        "code",
        "description",
        "tokens",
    ]

    search_fields = ["name", "code", "description"]


@admin.register(EmailTemplate)
class EmailTemplateModelAdmin(ModelAdminMixin):
    list_display = [
        "id",
        "name",
        "code",
        "content",
    ]

    search_fields = ["name", "code", "content"]
