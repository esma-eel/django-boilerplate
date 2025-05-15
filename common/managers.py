from django.db import models


class BaseManager(models.Manager):
    def get_queryset(self):
        return self._queryset_class(self.model, using=self._db).exclude(
            is_removed=True
        )

    def deleted(self):
        return self._queryset_class(self.model, using=self._db).filter(
            is_removed=True
        )

    def active(self):
        return self.get_queryset().filter(is_active=True)

    def deactive(self):
        return self.get_queryset().filter(is_active=False)

    def everything(self):
        return self._queryset_class(self.model, using=self._db)
