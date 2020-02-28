# type: ignore
# flake8: noqa

import os
import sys

from ecommerce.settings.base import *
from ecommerce.settings.base import (COMPREHENSIVE_THEME_DIRS, INSTALLED_APPS,
                                     JWT_AUTH, LOGGING, MIDDLEWARE_CLASSES)


# System
ALLOWED_HOSTS = ["*"]
TIME_ZONE = os.environ.get("TIME_ZONE", "UTC")
LANGUAGE_CODE = os.environ.get("LANGUAGE_CODE", "en")

SECRET_KEY = os.environ.get("SECRET_KEY", "replace-me")
EDX_API_KEY = os.environ.get("EDX_API_KEY", "replace-me")

LOGGING["handlers"]["local"] = {
    "level": "DEBUG",
    "class": "logging.StreamHandler",
    "formatter": "standard",
}

CACHES = {"default": {"BACKEND": "django.core.cache.backends.dummy.DummyCache",}}

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": os.environ.get("MYSQL_DB_NAME", "derex_ecommerce"),
        "USER": os.environ.get("MYSQL_DB_USER", "root"),
        "PASSWORD": os.environ.get("MYSQL_DB_PASSWORD", "secret"),
        "HOST": os.environ.get("MYSQL_DB_HOST", "mysql"),
        "PORT": os.environ.get("MYSQL_DB_PORT", 3306),
        "ATOMIC_REQUESTS": True,
        "CONN_MAX_AGE": 60,
    }
}

# Static files
STATIC_ROOT = "/openedx/staticfiles"
COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
COMPREHENSIVE_THEME_DIRS.append("/openedx/themes/")

# Authentication
SOCIAL_AUTH_EDX_OIDC_KEY = os.environ.get("SOCIAL_AUTH_EDX_OIDC_KEY", "ecommerce-key")
SOCIAL_AUTH_EDX_OIDC_SECRET = os.environ.get(
    "SOCIAL_AUTH_EDX_OIDC_SECRET", "ecommerce-secret"
)
SOCIAL_AUTH_EDX_OIDC_ID_TOKEN_DECRYPTION_KEY = SOCIAL_AUTH_EDX_OIDC_SECRET
SOCIAL_AUTH_EDX_OIDC_ISSUER = "http://lms.localhost:4700/oauth2"
SOCIAL_AUTH_EDX_OIDC_URL_ROOT = "http://lms.localhost:4700/oauth2"
SOCIAL_AUTH_EDX_OIDC_PUBLIC_URL_ROOT = "http://lms.localhost:4700/oauth2"
SOCIAL_AUTH_EDX_OIDC_LOGOUT_URL = "http://lms.localhost:4700/logout"
SOCIAL_AUTH_REDIRECT_IS_HTTPS = False

JWT_AUDIENCE = os.environ.get("JWT_AUDIENCE", "lms-key")
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "lms-secret")
JWT_AUTH.update(
    {
        "JWT_SECRET_KEY": JWT_SECRET_KEY,
        "JWT_ISSUERS": (
            {
                "ISSUER": SOCIAL_AUTH_EDX_OIDC_ISSUER,
                "AUDIENCE": JWT_AUDIENCE,
                "SECRET_KEY": JWT_SECRET_KEY,
            },
            {
                "ISSUER": "ecommerce_worker",
                "AUDIENCE": JWT_AUDIENCE,
                "SECRET_KEY": JWT_SECRET_KEY,
            },
        ),
    }
)

# Celery
# In order for tasks to be visible to the ecommerce worker, this must match the value of BROKER_URL
# configured for the ecommerce worker
CELERY_BROKER_VHOST = os.environ.get("CELERY_BROKER_VHOST", "/")
CELERY_BROKER_TRANSPORT = os.environ.get("CELERY_BROKER_TRANSPORT", "amqp")
CELERY_BROKER_HOSTNAME = os.environ.get("CELERY_BROKER_HOSTNAME", "rabbitmq")
CELERY_BROKER_USER = os.environ.get("CELERY_BROKER_USER", "guest")
CELERY_BROKER_PASSWORD = os.environ.get("CELERY_BROKER_PASSWORD", "guest")
BROKER_URL = "{0}://{1}:{2}@{3}/{4}".format(
    CELERY_BROKER_TRANSPORT,
    CELERY_BROKER_USER,
    CELERY_BROKER_PASSWORD,
    CELERY_BROKER_HOSTNAME,
    CELERY_BROKER_VHOST,
)

# Discovery
COURSE_CATALOG_API_URL = "http://discovery.localhost:4910/api/v1/"

if "runserver" in sys.argv:
    DEBUG = True
    COMPRESS_ENABLED = False
    COMPRESS_OFFLINE = False

    MIDDLEWARE_CLASSES += ("debug_toolbar.middleware.DebugToolbarMiddleware",)

    INSTALLED_APPS.append("debug_toolbar")
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": (lambda __: True),
        "DISABLE_PANELS": ("debug_toolbar.panels.template.TemplateDebugPanel",),
    }
    # Without this debug toolbar urls are not registered...
    os.environ["ENABLE_DJANGO_TOOLBAR"] = "1"
else:
    MIDDLEWARE_CLASSES += ("whitenoise.middleware.WhiteNoiseMiddleware",)

from .container_env import *  # isort:skip
