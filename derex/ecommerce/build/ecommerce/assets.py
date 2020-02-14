from .base import *

LOGGING["handlers"]["local"] = {
    "level": "DEBUG",
    "class": "logging.StreamHandler",
    "formatter": "standard"
}

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = True
