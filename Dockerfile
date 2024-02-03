FROM python:3.10

COPY . /hotel-bot
WORKDIR /hotel-bot

RUN apt-get update \
    && pip3 install --upgrade pip \
    && pip3 install --upgrade setuptools \
    && pip3 install .
RUN chmod 755 .
