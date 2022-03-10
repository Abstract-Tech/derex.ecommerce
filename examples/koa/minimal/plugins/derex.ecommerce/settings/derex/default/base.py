# type: ignore
# flake8: noqa

from derex_ecommerce_django.constants import DEREX_ECOMMERCE_SUPPORTED_VERSIONS
from ecommerce.settings.base import *

import os
import sys


try:
    DEREX_ECOMMERCE_VERSION = os.environ["DEREX_ECOMMERCE_VERSION"]
    assert DEREX_ECOMMERCE_VERSION in DEREX_ECOMMERCE_SUPPORTED_VERSIONS
except KeyError:
    raise RuntimeError(
        "DEREX_ECOMMERCE_VERSION environment variable must be defined in order to use derex default settings"
    )
except AssertionError:
    raise RuntimeError(
        "DEREX_ECOMMERCE_VERSION must be on of {}".format(
            DEREX_ECOMMERCE_SUPPORTED_VERSIONS
        )
    )

# System
ALLOWED_HOSTS = ["*"]
TIME_ZONE = os.environ.get("TIME_ZONE", "UTC")
LANGUAGE_CODE = os.environ.get("LANGUAGE_CODE", "en")
DEREX_PROJECT = os.environ["DEREX_PROJECT"]

SECRET_KEY = os.environ.get("SECRET_KEY", "replace-me")
EDX_API_KEY = os.environ.get("EDX_API_KEY", "replace-me")

LOGGING["handlers"]["local"] = {
    "level": "DEBUG",
    "class": "logging.StreamHandler",
    "formatter": "standard",
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

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
# Those are the SSO settings needed until ironwood release
SOCIAL_AUTH_EDX_OIDC_KEY = os.environ.get(
    "SOCIAL_AUTH_EDX_OIDC_KEY", "lms-ecommerce-sso-key"
)
SOCIAL_AUTH_EDX_OIDC_SECRET = os.environ.get(
    "SOCIAL_AUTH_EDX_OIDC_SECRET", "lms-ecommerce-sso-secret"
)
SOCIAL_AUTH_EDX_OIDC_ID_TOKEN_DECRYPTION_KEY = SOCIAL_AUTH_EDX_OIDC_SECRET
SOCIAL_AUTH_EDX_OIDC_ISSUER = "http://{}.localhost/oauth2".format(DEREX_PROJECT)
SOCIAL_AUTH_EDX_OIDC_URL_ROOT = SOCIAL_AUTH_EDX_OIDC_ISSUER
SOCIAL_AUTH_EDX_OIDC_PUBLIC_URL_ROOT = SOCIAL_AUTH_EDX_OIDC_ISSUER
SOCIAL_AUTH_EDX_OIDC_LOGOUT_URL = "http://{}.localhost/logout".format(DEREX_PROJECT)
SOCIAL_AUTH_REDIRECT_IS_HTTPS = False

# Those are the SSO settings needed from juniper onward
SOCIAL_AUTH_EDX_OAUTH2_KEY = os.environ.get(
    "SOCIAL_AUTH_EDX_OAUTH2_KEY", SOCIAL_AUTH_EDX_OIDC_KEY
)
SOCIAL_AUTH_EDX_OAUTH2_SECRET = os.environ.get(
    "SOCIAL_AUTH_EDX_OAUTH2_SECRET", SOCIAL_AUTH_EDX_OIDC_SECRET
)
SOCIAL_AUTH_EDX_OAUTH2_ISSUER = os.environ.get(
    "SOCIAL_AUTH_EDX_OAUTH2_ISSUER", SOCIAL_AUTH_EDX_OIDC_ISSUER
)
SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT = os.environ.get(
    "SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT", "http://{}.localhost".format(DEREX_PROJECT)
)
SOCIAL_AUTH_EDX_OAUTH2_LOGOUT_URL = os.environ.get(
    "SOCIAL_AUTH_EDX_OAUTH2_LOGOUT_URL", SOCIAL_AUTH_EDX_OIDC_LOGOUT_URL
)
BACKEND_SERVICE_EDX_OAUTH2_KEY = os.environ.get(
    "BACKEND_SERVICE_EDX_OAUTH2_KEY", "lms-ecommerce-backend-service-key"
)
BACKEND_SERVICE_EDX_OAUTH2_SECRET = os.environ.get(
    "BACKEND_SERVICE_EDX_OAUTH2_SECRET", "lms-ecommerce-backend-service-secret"
)

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

# Enterprise
ENTERPRISE_API_URL = "{}/enterprise/api/v1".format(SOCIAL_AUTH_EDX_OAUTH2_URL_ROOT)

# Discovery
COURSE_CATALOG_API_URL = "http://discovery.{}.localhost/api/v1/".format(DEREX_PROJECT)

if "runserver" in sys.argv:
    DEBUG = True
    COMPRESS_ENABLED = False
    COMPRESS_OFFLINE = False

    if DEREX_ECOMMERCE_VERSION == "ironwood":
        MIDDLEWARE_CLASSES += ("debug_toolbar.middleware.DebugToolbarMiddleware",)
    else:
        MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)

    INSTALLED_APPS.append("debug_toolbar")
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": (lambda __: True),
        "DISABLE_PANELS": ("debug_toolbar.panels.template.TemplateDebugPanel",),
    }
    # Without this debug toolbar urls are not registered...
    os.environ["ENABLE_DJANGO_TOOLBAR"] = "1"
else:
    if DEREX_ECOMMERCE_VERSION == "ironwood":
        MIDDLEWARE_CLASSES += ("whitenoise.middleware.WhiteNoiseMiddleware",)
    else:
        MIDDLEWARE += ("whitenoise.middleware.WhiteNoiseMiddleware",)

from .container_env import *  # isort:skip
