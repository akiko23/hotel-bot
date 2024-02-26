FROM python:3.10-alpine

COPY . /hotel-bot
WORKDIR /hotel-bot

RUN apk update \
    && pip3 install --upgrade pip \
    && pip3 install --upgrade setuptools \
    && pip3 install .
RUN chmod 755 .
