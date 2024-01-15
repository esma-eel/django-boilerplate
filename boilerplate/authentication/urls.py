from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from .forms import PasswordResetFormEmailChecker

app_name = "authentication"

urlpatterns = [
    path(
        "password-change/",
        auth_views.PasswordChangeView.as_view(),
        name="password-change",
    ),
    path(
        "password-change/done/",
        auth_views.PasswordChangeDoneView.as_view(),
        name="password-change-done",
    ),
    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            form_class=PasswordResetFormEmailChecker,
            success_url=reverse_lazy("authentication:password-reset-done"),
        ),
        name="password-reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password-reset-done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password-reset-complete",
    ),
    path(
        "login/",
        auth_views.LoginView.as_view(redirect_authenticated_user=True),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
