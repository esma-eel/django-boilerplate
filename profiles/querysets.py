from common.querysets import BaseQueryset


class ProfileQs(BaseQueryset):
    def email(self, email, active_only=False):
        return self._filter_field({"email": email}, active_only)

    def username(self, username, active_only=False):
        return self._filter_field({"user__username": username}, active_only)
