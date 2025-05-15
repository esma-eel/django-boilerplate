from django.db import models

class TimeStampMixin(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SoftDeleteMixin(models.Model):
    class Meta:
        abstract = True

    is_removed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.is_removed = True

        self.save()
    
    def recover(self, *args, **kwargs):
        self.is_active = True
        self.is_removed = False

        self.save()

    def purge(self, using=None, keep_parents=False):
        return super().delete(using=using, keep_parents=keep_parents)
    
    def is_deleted(self):
        return not self.is_active and self.is_removed


class BaseModel(SoftDeleteMixin, TimeStampMixin):
    class Meta:
        abstract = True
