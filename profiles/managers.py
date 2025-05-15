from common.managers import BaseManager
from .querysets import ProfileQs

class ProfileManager(BaseManager.from_queryset(ProfileQs)):
    use_in_migrations = True

    def email_exists(self, email, active_only=False):
        return self.email(email, active_only).exists()
    
    def get_by_email(self, email, active_only=False):
        return self.email(email, active_only).order_by("-id").first()
    
    def get_user_by_email(self, email, active_only=False):
        obj = self.get_by_email(email, active_only)
        if obj:
            return obj.user

        return None
    
    def get_by_username(self, username, active_only=True):
        return self.username(username, active_only).order_by("-id").first()

    def get_user_by_username(self, username, active_only=False):
        obj = self.get_by_username(username, active_only)
        if obj:
            return obj.user

        return None
