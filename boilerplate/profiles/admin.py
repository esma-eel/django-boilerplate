from django.contrib import admin
from .models import Profile, ProfileAddress, ProfileEmail, ProfilePhoneNumber

# Register your models here.
from boilerplate.common.mixins import ModelAdminMixin


class ProfileEmailAdminStackedInline(admin.StackedInline):
    model = ProfileEmail
    fk_name = "profile"
    extra = 0


class ProfilePhoneNumberAdminStackedInline(admin.StackedInline):
    model = ProfilePhoneNumber
    fk_name = "profile"
    extra = 0


class ProfileAddressAdminStackedInline(admin.StackedInline):
    model = ProfileAddress
    fk_name = "profile"
    extra = 0


@admin.register(Profile)
class ProfileAdminI(ModelAdminMixin):
    list_display = [
        "name",
        "user",
    ]

    readonly_fields = ["uuid"]

    inlines = [
        ProfileEmailAdminStackedInline,
        ProfilePhoneNumberAdminStackedInline,
        ProfileAddressAdminStackedInline,
    ]
