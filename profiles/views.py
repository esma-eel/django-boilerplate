from typing import Any
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.shortcuts import render
from django.views.generic import UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from .models import Profile
from .forms import (
    ProfileModelForm,
)


# Create your views here.
def profile_home(request, username=None):
    return render(
        request,
        template_name="profiles/profile.html",
    )


class ProfileView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Profile
    template_name = "profiles/profile.html"
    context_object_name = "profile"

    def test_func(self):
        user = self.request.user
        instance = self.get_object()

        if user.is_superuser or instance.user == user:
            return True

        return False

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        return get_object_or_404(
            queryset, user__username=self.kwargs.get("username")
        )
    
    def get_context_data(self, **kwargs):
        kwargs.setdefault("menu_item", "account")
        kwargs.setdefault("submenu_item", "view_profile")
        return super().get_context_data(**kwargs)



class ProfileEditView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, UpdateView
):
    template_name = "profiles/edit.html"
    model = Profile
    form_class = ProfileModelForm
    success_message = "Profile successfully updated!"

    def test_func(self):
        user = self.request.user
        instance = self.get_object()

        if user.is_superuser or instance.user == user:
            return True

        return False

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()

        return get_object_or_404(
            queryset, user__username=self.kwargs.get("username")
        )

    def get_success_url(self):
        profile_object = self.get_object()
        url = reverse(
            "profiles:profile",
            kwargs={"username": profile_object.user.username},
        )
        return url
    
    def get_context_data(self, **kwargs):
        kwargs.setdefault("menu_item", "account")
        kwargs.setdefault("submenu_item", "edit_profile")
        return super().get_context_data(**kwargs)
