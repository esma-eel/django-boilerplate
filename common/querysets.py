from django.db import models


class BaseQueryset(models.QuerySet):
    def _filter_field(self, kwargs, active_only=True):
        qs = self.filter(**kwargs)
        if active_only:
            return qs.exclude(is_active=False)
        return qs

    def delete(self):
        return self.update(is_removed=True, is_active=False)

    def purge(self):
        return super().delete()
    
    def recover(self):
        return self.update(is_removed=False, is_active=True)
