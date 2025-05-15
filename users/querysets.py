from django.db import models
from common.querysets import BaseQueryset


class UserQs(BaseQueryset):
    def username(self, username, active_only=False):
        return self._filter_field({"username": username}, active_only)
