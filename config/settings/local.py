"""
This is the settings file that you use when
you’re working on the project locally. Lo-
cal development-specific settings include
DEBUG mode, log level, and activation of
developer tools like django-debug-toolbar.
"""
from .base import *
from .production import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

INSTALLED_APPS += []
