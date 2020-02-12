FROM docker.io/python:2.7.16-alpine3.10
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

# Copy an already migrated db dump
# TODO: Remove backup from version control and
# do this step during CI build
COPY ./empty_dump.sql.bz2 ./openedx/empty_dump.sql.bz2

RUN mkdir -p /openedx/ecommerce
WORKDIR /openedx/ecommerce
RUN wget -O - https://github.com/edx/ecommerce/tarball/open-release/ironwood.master | \
    tar xzf - --strip-components 1

# Setup nodejs requirements
RUN npm install
RUN ./node_modules/.bin/bower install --allow-root

# Replace mysql-python with mysqlclient since
# i can't find a way to build mysql-python
RUN sed -i "s/mysql-python==1.2.5/mysqlclient/" requirements/production.txt

# Setup python requirements
RUN pip install -r requirements.txt

# Collect static assets
COPY ./settings.py ./ecommerce/settings/derex.py
ENV DJANGO_SETTINGS_MODULE ecommerce.settings.derex
RUN ./node_modules/.bin/r.js -o build.js
RUN make theme_static
RUN python manage.py collectstatic --noinput
RUN python manage.py compress --force

# Setup minimal yml config file, which is required by production settings
RUN echo "{}" > /openedx/config.yml
ENV ECOMMERCE_CFG /openedx/config.yml

EXPOSE 4900
CMD gunicorn \
    --bind=0.0.0.0:4900 \
    --workers 2 \
    --max-requests=1000 \
    ecommerce.wsgi:application
