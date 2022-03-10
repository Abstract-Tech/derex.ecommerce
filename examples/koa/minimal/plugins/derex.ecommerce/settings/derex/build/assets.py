"""
Bare minimum settings for collecting static assets
"""

from ecommerce.settings.base import *


STATIC_ROOT = "/openedx/staticfiles"

LOGGING["handlers"]["local"] = {
    "level": "DEBUG",
    "class": "logging.StreamHandler",
    "formatter": "standard",
}

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
