from django.contrib import admin
from .models import Profile

# Register your models here.
from common.admin import BaseModelAdmin


@admin.register(Profile)
class ProfileAdminI(BaseModelAdmin):
    list_display = [
        "name",
        "user",
        "email",
        "is_active",
    ]

    readonly_fields = ["user", "is_removed"]
