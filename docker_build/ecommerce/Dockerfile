# syntax = docker/dockerfile:experimental

ARG ALPINE_VERSION=alpine3.13
ARG PYTHON_VERSION=3.6
FROM docker.io/python:${PYTHON_VERSION}-${ALPINE_VERSION} as base
MAINTAINER Chiruzzi Marco <chiruzzi.marco@gmail.com>

RUN apk add \
    git \
    libffi-dev \
    libressl-dev \
    build-base \
    npm \
    nodejs \
    libxml2-dev \
    xmlsec-dev \
    jpeg-dev \
    zlib-dev

# Unfortunately this is required by mysql-python python package
# https://github.com/gliderlabs/docker-alpine/issues/181
RUN apk add mariadb-dev

ARG ECOMMERCE_RELEASE=koa
ARG ECOMMERCE_VERSION=open-release/koa.master
ARG ECOMMERCE_REPOSITORY=https://github.com/edx/ecommerce.git

RUN mkdir -p /openedx/ecommerce
WORKDIR /openedx/ecommerce
RUN git clone ${ECOMMERCE_REPOSITORY} --branch ${ECOMMERCE_VERSION} --depth 1 /openedx/ecommerce

# Setup nodejs requirements
RUN npm install
RUN ./node_modules/.bin/bower install --allow-root

# Replace mysql-python with mysqlclient since
# i can't find a way to build mysql-python
RUN sed -i "s/mysql-python==1.2.5/mysqlclient/" requirements/production.txt

# Setup python requirements
# TODO: Build a different image for development
RUN pip install -r requirements/dev.txt
RUN pip install -r requirements.txt

# By default pick the latest version
ARG WHITENOISE_VERSION=
RUN pip install "whitenoise$WHITENOISE_VERSION"

COPY ecommerce/derex_ecommerce_django/ /openedx/derex_ecommerce_django
RUN pip install /openedx/derex_ecommerce_django

# Include an already migrated mysql dump
# TODO: Remove backup from version control and
# do this step during CI build
RUN --mount=type=tmpfs,target=/mysql/var/lib/mysql \
    --mount=type=bind,from=docker.io/mysql:5.6.36,target=/mysql,rw=true \
    set -ex; \
    cp -a /dev/ /mysql; \
    export MYSQL_ALLOW_EMPTY_PASSWORD=1; \
    echo -e '[mysqld]\nport=3399\ncollation-server = utf8_general_ci\ncharacter-set-server = utf8' >> /mysql/etc/mysql/conf.d/custom_port.cnf; \
    chroot /mysql /usr/local/bin/docker-entrypoint.sh mysqld > /mysql/mysqld.out & \
    until grep "MySQL init process done. Ready for start up" /mysql/mysqld.out ; do sleep 1; done; \
    until chroot /mysql mysqladmin -P 3399 create ecommerce; do sleep 1; done; \
    export DJANGO_SETTINGS_MODULE="derex_ecommerce_django.settings.build.migration"; \
    python manage.py migrate; \
    chroot /mysql mysqldump ecommerce | bzip2 -9 - > /openedx/empty_dump.sql.bz2;

# Collect static assets
RUN ./node_modules/.bin/r.js -o build.js
RUN DJANGO_SETTINGS_MODULE=derex_ecommerce_django.settings.build.assets python manage.py update_assets --skip-collect
RUN DJANGO_SETTINGS_MODULE=derex_ecommerce_django.settings.build.assets python manage.py collectstatic --noinput
RUN DJANGO_SETTINGS_MODULE=derex_ecommerce_django.settings.build.assets python manage.py compress --force

RUN mkdir -p /openedx/themes

# Setup minimal yml config file, which is required by production settings
RUN echo "{}" > /openedx/config.yml
ENV ECOMMERCE_CFG /openedx/config.yml
ENV DJANGO_SETTINGS_MODULE=derex_ecommerce_django.settings.default.base
ENV DEREX_ECOMMERCE_VERSION=${ECOMMERCE_RELEASE}

EXPOSE 80
COPY ecommerce/wsgi_whitenoise.py ecommerce/wsgi_whitenoise.py
CMD gunicorn \
    --bind=0.0.0.0:80 \
    --workers 2 \
    --max-requests=1000 \
    ecommerce.wsgi_whitenoise:application
