ARG ALPINE_VERSION=alpine3.13
ARG PYTHON_VERSION=3.6
FROM docker.io/python:${PYTHON_VERSION}-${ALPINE_VERSION} as base
MAINTAINER Chiruzzi Marco <chiruzzi.marco@gmail.com>

RUN apk add git gcc musl-dev libc-dev linux-headers

ARG ECOMMERCE_RELEASE=koa
ARG ECOMMERCE_VERSION=open-release/koa.master
ARG ECOMMERCE_WORKER_REPOSITORY=https://github.com/edx/ecommerce-worker.git

RUN mkdir -p /openedx/ecommerce_worker
WORKDIR /openedx/ecommerce_worker
RUN git clone ${ECOMMERCE_WORKER_REPOSITORY} --branch ${ECOMMERCE_VERSION} --depth 1 /openedx/ecommerce_worker

# Install python requirements
RUN pip install -r requirements/production.txt
COPY ecommerce_worker/settings.py ecommerce_worker/configuration/derex.py

ENV WORKER_CONFIGURATION_MODULE ecommerce_worker.configuration.derex
CMD celery worker \
    --app=ecommerce_worker.celery_app:app \
    --loglevel=info \
    --maxtasksperchild 100 \
    --queue=fulfillment,email_marketing
