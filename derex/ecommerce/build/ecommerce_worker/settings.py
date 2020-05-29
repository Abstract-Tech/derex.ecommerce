import os

from ecommerce_worker.configuration.base import *


ECOMMERCE_API_ROOT = os.environ.get("ECOMMERCE_API_ROOT", "http://ecommerce.{}.localhost/api/v2/").format(DEREX_PROJECT)

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "lms-secret")

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

CELERY_RESULT_BACKEND = None
