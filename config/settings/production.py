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
# U hsould set variables below like the ones you set in environment variables
REDIS_HOST = "localhost"
REDIS_PORT = "6379"
REDIS_DB = 0  # IDK why we should use this yet
REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}"

CELERY_BROKER_URL = get_env_variable_with_default(
    "CELERY_BROKER_URL", REDIS_URL
)

# save Celery task results in Django's database
CELERY_RESULT_BACKEND = "django-db"

# this allows you to schedule items in the Django admin.
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers.DatabaseScheduler"
