"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 3.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from datetime import timedelta
import os
import environ
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    ON_SERVER=(bool, True), LOGGING_LEVEL=(str, "INFO"), DEBUG=(bool, False)
)

IGNORE_DOT_ENV_FILE = env.bool("IGNORE_DOT_ENV_FILE", default=False)
if not IGNORE_DOT_ENV_FILE:
    # reading .env file
    environ.Env.read_env(env_file=os.path.join(BASE_DIR, ".env"))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DEBUG")
ON_SERVER = env("ON_SERVER", default=True)


ALLOWED_HOSTS = ["*"]
CORS_ALLOW_CREDENTIALS = True
if ON_SERVER:
    CORS_ORIGIN_REGEX_WHITELIST = env.list("CORS_ORIGIN_REGEX_WHITELIST", default=[])
else:
    CORS_ORIGIN_ALLOW_ALL = True

# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
]

THIRD_PARTY_APPS = [
    "corsheaders",
    "axes",
    "django_extensions",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "drf_yasg",
]

AUTHENTICATION_THIRD_PARTY_APPS = [
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.google",
]

OUR_APPS = [
    "users.apps.UsersConfig",
]


INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + AUTHENTICATION_THIRD_PARTY_APPS + OUR_APPS

AUTHENTICATION_BACKENDS = [
    # AxesBackend should be the first backend in the AUTHENTICATION_BACKENDS list.
    "axes.backends.AxesBackend",
    # Django ModelBackend is the default authentication backend.
    "django.contrib.auth.backends.ModelBackend",
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

# we are turning off email verification for now
SOCIALACCOUNT_EMAIL_VERIFICATION = "none"
SOCIALACCOUNT_EMAIL_REQUIRED = False

SITE_ID = 1  # https://dj-rest-auth.readthedocs.io/en/latest/installation.html#registration-optional
REST_USE_JWT = True  # use JSON Web Tokens
# JWT_AUTH_COOKIE = "nextjsdrf-access-token"
# JWT_AUTH_REFRESH_COOKIE = "nextjsdrf-refresh-token"
# JWT_AUTH_SAMESITE = "none"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # AxesMiddleware should be the last middleware in the MIDDLEWARE list.
    # It only formats user lockout messages and renders Axes lockout responses
    # on failed user authentication attempts from login views.
    # If you do not want Axes to override the authentication response
    # you can skip installing the middleware and use your own views.
    "axes.middleware.AxesMiddleware",
]

if not ON_SERVER:
    INSTALLED_APPS.append("debug_toolbar")
    MIDDLEWARE.insert(9, "debug_toolbar.middleware.DebugToolbarMiddleware")
    INTERNAL_IPS = [
        "127.0.0.1",
    ]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": env.db(),
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

PASSWORD_VALIDATORS = [
    "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    "django.contrib.auth.password_validation.MinimumLengthValidator",
    "django.contrib.auth.password_validation.CommonPasswordValidator",
    "django.contrib.auth.password_validation.NumericPasswordValidator",
]

AUTH_PASSWORD_VALIDATORS = [{"NAME": v} for v in PASSWORD_VALIDATORS]
AUTH_USER_MODEL = "users.CustomUser"
# We need to specify the exact serializer as well for dj-rest-auth, otherwise it will end up shooting itself
# in the foot and me in the head
REST_AUTH_SERIALIZERS = {
    'USER_DETAILS_SERIALIZER': 'users.serializers.CustomUserModelSerializer'
}

# CUSTOM USER MODEL::: Dajngo allauth We need to specify custom user model
# https://django-allauth.readthedocs.io/en/latest/advanced.html

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATIC_URL = "/static/"

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


if ON_SERVER:
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
    STATIC_URL = "/static/"
    MIDDLEWARE = tuple(
        ["whitenoise.middleware.WhiteNoiseMiddleware"] + list(MIDDLEWARE)
    )
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": (
                "%(asctime)s [%(process)d] [%(levelname)s] "
                + "pathname=%(pathname)s lineno=%(lineno)s "
                + "funcname=%(funcName)s %(message)s"
            ),
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "null": {
            "level": "DEBUG",
            "class": "logging.NullHandler",
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "app": {
            "handlers": ["console"],
            "level": env("LOGGING_LEVEL"),
        }
    },
}


REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ),
}


# AXES::: Total number of attempts before the user gets locked out.
AXES_FAILURE_LIMIT = 10

# TODO: JWT::: Settings, change and remove secret key
# https://github.com/mahieyin-rahmun/NextJsWithDRFExample/blob/main/backend/nextjsdrfbackend/settings.py

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "USER_ID_FIELD": "id",  # for the custom user model
    "USER_ID_CLAIM": "Id",
}

JWT_COOKIE_NAME = env.str("JWT_COOKIE_NAME", default="refresh_token")
JWT_COOKIE_SECURE = env.bool("JWT_COOKIE_SECURE", default=False)
JWT_COOKIE_SAMESITE = env.str("JWT_COOKIE_SAMESITE", default="Lax")


if ON_SERVER:
    # HTTPS
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = True
