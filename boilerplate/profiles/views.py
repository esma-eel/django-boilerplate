from django.shortcuts import render
from .forms import (
    ProfileModelForm,
    # ProfilePhoneNumberModelFormSet,
    # ProfileEmailModelFormSet,
)


# Create your views here.
def profile_home(request, username=None):
    return render(
        request,
        template_name="profiles/profile.html",
    )


def profile_view(request, username=None):
    return render(
        request,
        template_name="profiles/profile.html",
    )


def profile_edit_view(request, username):
    return render(
        request,
        template_name="profiles/edit.html",
        context={"form": ProfileModelForm()},
    )
