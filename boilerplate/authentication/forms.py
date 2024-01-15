from django.contrib.auth.forms import PasswordResetForm
from django.core.validators import ValidationError
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
