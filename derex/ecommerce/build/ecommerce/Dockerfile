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
COPY ./empty_dump.sql.bz2 /openedx/empty_dump.sql.bz2

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
# TODO: Build a different image for development
RUN pip install -r requirements/dev.txt
RUN pip install -r requirements.txt
RUN pip install whitenoise==4.1.3

# Collect static assets
COPY ./assets.py ./ecommerce/settings/assets.py
ENV DJANGO_SETTINGS_MODULE ecommerce.settings.assets
RUN ./node_modules/.bin/r.js -o build.js
RUN python manage.py update_assets --skip-collect
RUN python manage.py collectstatic --noinput
RUN python manage.py compress --force

RUN mkdir -p /openedx/themes

# Setup minimal yml config file, which is required by production settings
RUN echo "{}" > /openedx/config.yml
ENV ECOMMERCE_CFG /openedx/config.yml

EXPOSE 4900
COPY ./wsgi_whitenoise.py ./ecommerce/wsgi_whitenoise.py
CMD gunicorn \
    --bind=0.0.0.0:4900 \
    --workers 2 \
    --max-requests=1000 \
    ecommerce.wsgi_whitenoise:application
