"""
This is the settings file used by your live
production server(s). That is, the server(s)
that host the real live website. This file con-
tains production-level settings only. It is
sometimes called prod.py.
"""

import os
from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_env_variable("SECRET_KEY")

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Celery and Redis
CELERY_BROKER_URL = get_env_variable_with_default(
    "CELERY_BROKER_URL", "redis://localhost:6379"
)

# save Celery task results in Django's database
CELERY_RESULT_BACKEND = "django-db"

# this allows you to schedule items in the Django admin.
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'
