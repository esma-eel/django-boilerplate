from django.contrib.auth.forms import PasswordResetForm
from django.core.validators import ValidationError
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from boilerplate.common.utils.generators import default_token_generator
from boilerplate.profiles.models import ProfileEmail


class PasswordResetFormEmailChecker(PasswordResetForm):
    def clean_email(self):
        to_email = self.cleaned_data.get("email")
        query_set = ProfileEmail.objects.filter(
            email=to_email, is_verified=True, is_primary=True
        )

        if not query_set.exists():
            raise ValidationError("Verified Primary Email not found!")

        return to_email

    def save(
        self,
        domain_override=None,
        subject_template_name="registration/password_reset_subject.txt",
        email_template_name="registration/password_reset_email.html",
        use_https=False,
        token_generator=default_token_generator,
        from_email=None,
        request=None,
        html_email_template_name=None,
        extra_email_context=None,
    ):
        email = self.cleaned_data["email"]
        if not domain_override:
            current_site = get_current_site(request)
            site_name = current_site.name
            domain = current_site.domain
        else:
            site_name = domain = domain_override

        qs = ProfileEmail.objects.filter(
            email=email, is_verified=True, is_primary=True
        )

        if qs.exists():
            profile_email_object = qs.last()
            profile_object = profile_email_object.profile
            user = profile_object.user
            context = {
                "email": email,
                "domain": domain,
                "site_name": site_name,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                "token": default_token_generator.make_token(user),
                "protocol": "https" if use_https else "http",
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name,
                email_template_name,
                context,
                from_email,
                email,
                html_email_template_name=html_email_template_name,
            )
