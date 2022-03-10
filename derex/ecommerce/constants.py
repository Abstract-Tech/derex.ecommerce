from derex.runner.utils import abspath_from_egg
from enum import Enum


DEREX_ECOMMERCE_DJANGO_PATH = abspath_from_egg(
    "derex.ecommerce", "derex/ecommerce_django/__init__.py"
).parent
DEREX_ECOMMERCE_DJANGO_SETTINGS_PATH = DEREX_ECOMMERCE_DJANGO_PATH / "settings"

DDC_PROJECT_TEMPLATE_PATH = abspath_from_egg(
    "derex.ecommerce", "derex/ecommerce/docker-compose-ecommerce.yml.j2"
)

assert all(
    (
        DDC_PROJECT_TEMPLATE_PATH,
        DEREX_ECOMMERCE_DJANGO_PATH,
        DEREX_ECOMMERCE_DJANGO_SETTINGS_PATH,
    )
), "Some distribution files were not found"


class EcommerceVersions(Enum):
    # Values will be passed as uppercased named arguments to the docker build
    # e.g. --build-arg ECOMMERCE_RELEASE=koa
    ironwood = {
        "ecommerce_repository": "https://github.com/edx/ecommerce.git",
        "ecommerce_version": "open-release/ironwood.master",
        "ecommerce_release": "ironwood",
        "docker_image_prefix": "ghcr.io/abstract-tech/derex-ecommerce-ironwood",
        "worker_docker_image_prefix": "ghcr.io/abstract-tech/derex-ecommerce-worker-ironwood",
        "alpine_version": "alpine3.11",
        "python_version": "2.7.18",
        "whitenoise_version": "<5.0",
    }
    juniper = {
        "ecommerce_repository": "https://github.com/edx/ecommerce.git",
        "ecommerce_version": "open-release/juniper.master",
        "ecommerce_release": "juniper",
        "docker_image_prefix": "ghcr.io/abstract-tech/derex-ecommerce-juniper",
        "worker_docker_image_prefix": "ghcr.io/abstract-tech/derex-ecommerce-worker-juniper",
        "alpine_version": "alpine3.13",
        "python_version": "3.8",
    }
    koa = {
        "ecommerce_repository": "https://github.com/edx/ecommerce.git",
        "ecommerce_version": "open-release/koa.master",
        "ecommerce_release": "koa",
        "docker_image_prefix": "ghcr.io/abstract-tech/derex-ecommerce-koa",
        "worker_docker_image_prefix": "ghcr.io/abstract-tech/derex-ecommerce-worker-koa",
        "alpine_version": "alpine3.13",
        "python_version": "3.8",
    }
