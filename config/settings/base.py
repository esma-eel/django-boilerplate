"""
Django settings for django_boilerplate project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/

Settings common to all instances of the
project
"""

import os
import environ
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse_lazy
from datetime import timedelta


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_FILE_PATH = Path(__file__)
# index starts from 0
BASE_DIR = BASE_FILE_PATH.parents[2]

# Take environment variables from .env file
env = environ.Env(SECRET_KEY=(str, "default"))
CONFIG_MODULE_PATH = os.path.join(BASE_DIR, "config")
ENV_DIR = os.path.join(CONFIG_MODULE_PATH, ".envs")
DEFAULT_ENV_PATH = os.path.join(ENV_DIR, ".env.default")
env.read_env(DEFAULT_ENV_PATH)


def get_env_variable(var_name, file=None):
    """
    Get environment variable or return exception
    """
    try:
        if file:
            env.read_env(file)
        # return os.environ[var_name]
        return env(var_name)
    except KeyError:
        error_msg = f"Set the {var_name} ENV variable."
        raise ImproperlyConfigured(error_msg)


def get_env_variable_with_default(var_name, default, file=None):
    try:
        result = get_env_variable(var_name, file)
        return result
    except (ImproperlyConfigured, KeyError):
        return default


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(get_env_variable("DEBUG"))
SECRET_KEY = get_env_variable("SECRET_KEY")

ALLOWED_HOSTS = get_env_variable("ALLOWED_HOSTS").split(" ")


# Application definition

INSTALLED_APPS = [
    # 3rd party
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "django_filters",
    "django_extensions",
    "corsheaders",
    "django_celery_beat",
    "django_celery_results",
    "drf_yasg",
    # boilerplate
    "boilerplate.users",
    "boilerplate.profiles",
    "boilerplate.authentication",
    "boilerplate.communications",
    "boilerplate.adminstration",
    "boilerplate.dashboard",
    # django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    # cors
    "corsheaders.middleware.CorsMiddleware",
    # should be on top of common middleware
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
# main database is in production.py
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation.NumericPasswordValidator"
        ),
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Tehran"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


MEDIA_ROOT = BASE_DIR / "_media"
STATIC_ROOT = BASE_DIR / "_static_root"
# general static file dirs --> developer puts statics here
STATICFILES_DIRS = [BASE_DIR / "static"]


STATIC_URL = "static/"
MEDIA_URL = "media/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "users.User"

# REST FRAMEWORK SETTINGS
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        # "rest_framework.authentication.BasicAuthentication",
        # "rest_framework.authentication.TokenAuthentication",
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.AllowAny"],
    "DEFAULT_THROTTLE_CLASSES": [],
    "DEFAULT_CONTENT_NEGOTIATION_CLASS": (
        "rest_framework.negotiation.DefaultContentNegotiation"
    ),
    "DEFAULT_METADATA_CLASS": "rest_framework.metadata.SimpleMetadata",
    "DEFAULT_VERSIONING_CLASS": None,
    "DEFAULT_PAGINATION_CLASS": (  # None,
        "rest_framework.pagination.LimitOffsetPagination"
    ),
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ],
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.openapi.AutoSchema",
    "DEFAULT_THROTTLE_RATES": {"user": None, "anon": None},
    "NUM_PROXIES": None,
    "PAGE_SIZE": 10,  # None
    "SEARCH_PARAM": "search",
    "ORDERING_PARAM": "ordering",
    "DEFAULT_VERSION": None,
    "ALLOWED_VERSIONS": None,
    "VERSION_PARAM": "version",
    "UNAUTHENTICATED_USER": "django.contrib.auth.models.AnonymousUser",
    "UNAUTHENTICATED_TOKEN": None,
    "VIEW_NAME_FUNCTION": "rest_framework.views.get_view_name",
    "VIEW_DESCRIPTION_FUNCTION": "rest_framework.views.get_view_description",
    "EXCEPTION_HANDLER": "rest_framework.views.exception_handler",
    "NON_FIELD_ERRORS_KEY": "non_field_errors",
    "TEST_REQUEST_RENDERER_CLASSES": [
        "rest_framework.renderers.MultiPartRenderer",
        "rest_framework.renderers.JSONRenderer",
    ],
    "TEST_REQUEST_DEFAULT_FORMAT": "multipart",
    "URL_FORMAT_OVERRIDE": "format",
    "FORMAT_SUFFIX_KWARG": "format",
    "URL_FIELD_NAME": "url",
    "DATE_FORMAT": "iso-8601",
    "DATE_INPUT_FORMATS": ["iso-8601"],
    "DATETIME_FORMAT": "iso-8601",
    "DATETIME_INPUT_FORMATS": ["iso-8601"],
    "TIME_FORMAT": "iso-8601",
    "TIME_INPUT_FORMATS": ["iso-8601"],
    "UNICODE_JSON": True,
    "COMPACT_JSON": True,
    "STRICT_JSON": True,
    "COERCE_DECIMAL_TO_STRING": True,
    "UPLOADED_FILES_USE_URL": True,
    "HTML_SELECT_CUTOFF": 1000,
    "HTML_SELECT_CUTOFF_TEXT": "More than {count} items...",
    "SCHEMA_COERCE_PATH_PK": True,
    "SCHEMA_COERCE_METHOD_NAMES": {"retrieve": "read", "destroy": "delete"},
}


# CORS SETTINGS
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:1337",
]
CORS_URLS_REGEX = r"^/api/.*$"
CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)
CORS_ALLOW_HEADERS = (
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
)
"""
CORS_ALLOWED_ORIGIN_REGEXES = [r"^https://\w+\.example\.com$"] #noqa
"""

# SIMPLE JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),  # timedelta(minutes=5),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=2),  # timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": (
        "rest_framework_simplejwt.authentication"
        ".default_user_authentication_rule"
    ),
    "AUTH_TOKEN_CLASSES": (
        "rest_framework_simplejwt.tokens.AccessToken",
        "rest_framework_simplejwt.tokens.SlidingToken",
    ),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
    "TOKEN_OBTAIN_SERIALIZER": (
        "rest_framework_simplejwt.serializers.TokenObtainPairSerializer"
    ),
    "TOKEN_REFRESH_SERIALIZER": (
        "rest_framework_simplejwt.serializers.TokenRefreshSerializer"
    ),
    "TOKEN_VERIFY_SERIALIZER": (
        "rest_framework_simplejwt.serializers.TokenVerifySerializer"
    ),
    "TOKEN_BLACKLIST_SERIALIZER": (
        "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
        # "authentication.api.serializers.JWTTokenBlacklistSerializer",
        # "authentication.api.serializers.SlidingTokenBlacklistSerializer",
    ),
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": (
        "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer"
    ),
    "SLIDING_TOKEN_REFRESH_SERIALIZER": (
        "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer"
    ),
}

# SECURITY WARNING: keep the secret key used in production secret!

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {"default": env.db_url("DATABASE_URL")}

# Celery and Redis
# U hsould set variables below like the ones you set in environment variables

REDIS_HOST = get_env_variable("REDIS_HOST")
REDIS_PORT = get_env_variable("REDIS_PORT")
REDIS_DB = get_env_variable("REDIS_DB")

CELERY_BROKER_URL = get_env_variable("REDIS_URL")

# save Celery task results in Django's database
CELERY_RESULT_BACKEND = "django-db"

# this allows you to schedule items in the Django admin.
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers.DatabaseScheduler"

# Authentication
LOGIN_URL = "authentication:login"
LOGOUT_URL = "authentication:logout"
# LOGIN_REDIRECT_URL = "profiles:profile"
LOGOUT_REDIRECT_URL = "authentication:login"
# in order to define absoulte url for models
# you have enter appname.model then like template below
ABSOLUTE_URL_OVERRIDES = {
    "users.user": lambda user: reverse_lazy(
        "profiles:profile", args=[user.username]
    )
}
