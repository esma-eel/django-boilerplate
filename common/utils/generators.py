from django.contrib.auth.tokens import PasswordResetTokenGenerator


class PasswordResetTokenGeneratorByProfileEmail(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        login_timestamp = (
            ""
            if user.last_login is None
            else user.last_login.replace(microsecond=0, tzinfo=None)
        )
        email = user.profile.email
        return f"{user.pk}{user.password}{login_timestamp}{timestamp}{email}"


default_token_generator = PasswordResetTokenGeneratorByProfileEmail()
