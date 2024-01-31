"""
This is the settings file that you use when
you’re working on the project locally. Lo-
cal development-specific settings include
DEBUG mode, log level, and activation of
developer tools like django-debug-toolbar.
"""
from .base import *  # noqa

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "127.0.0.1"
EMAIL_PORT = 1025
# EMAIL_USE_TLS = True
EMAIL_HOST_USER = "user@localhost"
EMAIL_HOST_PASSWORD = "password"
PROJECT_EMAIL = EMAIL_HOST_USER

INSTALLED_APPS += []  # noqa

TEST_RUNNER = "redgreenunittest.django.runner.RedGreenDiscoverRunner"
print("local")
