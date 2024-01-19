from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
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


class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "profiles/profile.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        return get_object_or_404(
            queryset, user__username=self.kwargs.get("username")
        )


class ProfileEditView(LoginRequiredMixin, UpdateView):
    template_name = "profiles/edit.html"
    model = Profile
    form_class = ProfileModelForm

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        return get_object_or_404(
            queryset, user__username=self.kwargs.get("username")
        )

    def get_success_url(self):
        url = reverse(
            "profiles:profile", kwargs={"username": self.object.user.username}
        )
        return url
