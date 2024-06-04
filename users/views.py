from typing import Any
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from .forms import UserCreationForm

User = get_user_model()


class UserCreateView(LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin, CreateView):
    form_class = UserCreationForm
    http_method_names = ["get", "post"]

    model = User
    template_name = "users/create.html"
    success_message = "User created succesfully"

    def test_func(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return True

        return False

    def get_success_url(self):
        url = reverse(
            "profiles:profile-edit", kwargs={"username": self.object.username}
        )
        return url
    
    def get_context_data(self, **kwargs):
        kwargs.setdefault("menu_item", "users")
        kwargs.setdefault("submenu_item", "view_create_user")
        return super().get_context_data(**kwargs)



class UserRegisterView(CreateView):
    form_class = UserCreationForm
    http_method_names = ["get", "post"]

    model = User
    template_name = "users/register.html"

    def get_success_url(self):
        url = reverse(
            "profiles:profile-edit", kwargs={"username": self.object.username}
        )
        return url


class UserListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    http_method_names = ["get"]
    model = User
    template_name = "users/list.html"

    def test_func(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return True

        return False

    def get_context_data(self, **kwargs):
        kwargs.setdefault("menu_item", "users")
        kwargs.setdefault("submenu_item", "view_list_user")
        return super().get_context_data(**kwargs)