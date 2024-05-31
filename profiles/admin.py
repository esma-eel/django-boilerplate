from django.contrib import admin
from .models import Profile

# Register your models here.
from common.mixins import ModelAdminMixin


@admin.register(Profile)
class ProfileAdminI(ModelAdminMixin):
    list_display = [
        "name",
        "user",
        "email",
        "phone_number",
        "city",
        "address",
        "is_active",
    ]

    readonly_fields = ["user", "is_removed"]
