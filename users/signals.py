from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

from profiles.models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created or not hasattr(instance, "profile"):
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def bind_profile(sender, instance, **kwargs):
    profile = instance.profile
    profile.is_active = instance.is_active
    profile.is_removed = instance.is_removed
    profile.save()

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    profile = instance.profile
    profile.save()
