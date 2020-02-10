FROM docker.io/python:2.7.16-alpine3.10
MAINTAINER Chiruzzi Marco <chiruzzi.marco@gmail.com>

RUN mkdir -p /openedx/ecommerce_worker
WORKDIR /openedx/ecommerce_worker
RUN wget -O - https://github.com/edx/ecommerce-worker/tarball/open-release/ironwood.master | \
    tar xzf - --strip-components 1

# Install python venv
RUN pip install -r requirements/production.txt
COPY ./settings.py ./ecommerce_worker/configuration/derex.py

ENV WORKER_CONFIGURATION_MODULE ecommerce_worker.configuration.derex
CMD celery worker \
    --app=ecommerce_worker.celery_app:app \
    --loglevel=info \
    --maxtasksperchild 100 \
    --queue=fulfillment,email_marketing
