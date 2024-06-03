from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic import UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from common.utils.otp_helpers import (
    generate_otp_for_receiver,
    send_otp_to_receiver_sms,
    send_otp_to_receiver_email,
)
from .models import Profile
from .forms import (
    ProfileModelForm,
    ProfileVerifyOTPForReceiver,
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


def send_otp_to_profile_phone_number_view(request):
    user = request.user
    profile = user.profile
    if not profile.phone_number_is_verified:
        phone_number = user.profile.phone_number
        otp = generate_otp_for_receiver(phone_number)
        success = send_otp_to_receiver_sms(phone_number, otp)
        if success:
            return redirect("profiles:verify-phone-number")
        else:
            messages.error(
                request,
                "OTP not sent for {phone_number}. try again".format(
                    phone_number=phone_number
                ),
            )
            return redirect("dashboard:dashboard")

    messages.error(request, "you alread verified your phone number!")
    return redirect("dashboard:dashboard")


def verify_profile_phone_number_view(request):
    post = "POST"
    profile = request.user.profile
    if not profile.phone_number_is_verified:
        if request.method == post:
            form = ProfileVerifyOTPForReceiver(
                request.POST, receiver=profile.phone_number
            )
            if form.is_valid():
                profile.phone_number_is_verified = True
                profile.save()
                messages.success(request, "Phone number verified successfully")
                return redirect("dashboard:dashboard")
        else:
            form = ProfileVerifyOTPForReceiver()

        context = {"form": form}

        return render(request, "profiles/verify_otp.html", context=context)

    messages.error(request, "you alread verified your phone number!")
    return redirect("dashboard:dashboard")


def send_otp_to_profile_email_view(request):
    user = request.user
    profile = user.profile
    if not profile.email_is_verified:
        email = user.profile.email
        otp = generate_otp_for_receiver(email)
        success = send_otp_to_receiver_email(email, otp)
        if success:
            return redirect("profiles:verify-email")
        else:
            messages.error(
                request,
                "OTP not sent for {email}. try again".format(
                    email=email
                ),
            )
            return redirect("dashboard:dashboard")

    messages.error(request, "you alread verified your email!")
    return redirect("dashboard:dashboard")


def verify_profile_email_view(request):
    post = "POST"
    profile = request.user.profile
    if not profile.email_is_verified:
        if request.method == post:
            form = ProfileVerifyOTPForReceiver(
                request.POST, receiver=profile.email
            )
            if form.is_valid():
                profile.email_is_verified = True
                profile.save()
                messages.success(request, "Email verified successfully")
                return redirect("dashboard:dashboard")
        else:
            form = ProfileVerifyOTPForReceiver()

        context = {"form": form}

        return render(request, "profiles/verify_otp.html", context=context)

    messages.error(request, "you alread verified your email!")
    return redirect("dashboard:dashboard")
