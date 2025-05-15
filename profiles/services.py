from .models import Profile


class ProfileService:
    @staticmethod
    def get_profile_by_username(username):
        return Profile.objects.get_by_username(username)
