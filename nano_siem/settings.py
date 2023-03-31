"""
Django settings for nano_siem project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG") == "True"

ALLOWED_HOSTS = [
    os.getenv("DOMAIN_NAME", "localhost"),
]
CSRF_TRUSTED_ORIGINS = [
    os.getenv("URL", "http://localhost:8000"),
]

USE_X_FORWARDED_HOST = os.getenv("USE_X_FORWARDED_HOST") == "True"
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Application definition

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

INSTALLED_APPS = [
    "django.contrib.auth",
    "mozilla_django_oidc",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_crontab",
    "main",
    "plugins.overwatch",
    "plugins.http_logs",
    "main.notifications",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# OIDC configuration
OIDC_RP_CLIENT_ID = os.getenv("OIDC_CLIENT_ID", "")
OIDC_RP_CLIENT_SECRET = os.getenv("OIDC_CLIENT_SECRET", "")
OIDC_OP_AUTHORIZATION_ENDPOINT = os.getenv("OIDC_AUTHORIZATION_ENDPOINT", "")
OIDC_OP_TOKEN_ENDPOINT = os.getenv("OIDC_TOKEN_ENDPOINT", "")
OIDC_OP_USER_ENDPOINT = os.getenv("OIDC_USER_ENDPOINT", "")
OIDC_OP_JWKS_ENDPOINT = os.getenv("OIDC_JWKS_ENDPOINT", "")

OIDC_RP_SIGN_ALGO = "RS256"
LOGIN_URL = "login_proxy"
LOGIN_REDIRECT_URL = "/"
OIDC_STORE_ID_TOKEN = True
OIDC_OP_LOGOUT_URL_METHOD = "main.user_authentication.user_logout"

# Add 'mozilla_django_oidc' authentication backend
AUTHENTICATION_BACKENDS = [
    "main.user_authentication.CustomAuthenticationBackend",
    "django.contrib.auth.backends.ModelBackend",
]

ROOT_URLCONF = "nano_siem.urls"

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
                "main.context_processors.template_env_vars",
            ],
        },
    },
]

WSGI_APPLICATION = "nano_siem.wsgi.application"

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.getenv("MYSQL_DB_NAME"),
        "USER": os.getenv("MYSQL_USER"),
        "PASSWORD": os.getenv("MYSQL_PASSWORD"),
        "HOST": os.getenv("MYSQL_HOST", "127.0.0.1"),
        "PORT": os.getenv("MYSQL_PORT", "3306"),
        "OPTIONS": {
            "sql_mode": "STRICT_ALL_TABLES",
        },
    }
}

# Keep the database connection open to improve performance
CONN_MAX_AGE = True

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = os.getenv("TIME_ZONE", "UTC")

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Cronjob configuration
CRONJOBS = [
    (
        "*/1 * * * *",
        "main.cronjob.cronjob",
        ">> /home/NanoSiem/.nano_siem/crontab.log 2>&1",
    )
]

# Logging configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "{name} | {levelname} | {asctime} | {message}",
            "style": "{",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
        "plugins": {
            "handlers": ["console"],
            "level": os.getenv("PLUGINS_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
        "main": {
            "handlers": ["console"],
            "level": os.getenv("MAIN_LOG_LEVEL", "INFO"),
            "propagate": False,
        },
        "mozilla_django_oidc": {
            "handlers": ["console"],
            "level": os.getenv("MOZILLA_OIDC_LOG_LEVEL", "INFO"),
        },
    },
}
