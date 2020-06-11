# FROM ubuntu:20.04
FROM python:3.8

RUN echo 'running the main dockerfile'
ARG DEBIAN_FRONTEND=noninteractive
ENV PYTHONBUFFERED 1

WORKDIR /app

RUN pwd
COPY . ./
RUN ls ./

RUN apt-get update \
    && apt-get install -y libdbus-1-dev libcups2-dev libgirepository1.0-dev
RUN apt-get install -y tesseract-ocr libudev-dev libsystemd-dev
    #python3 python3-pip libdbus-glib-1-dbus

RUN pip3 install --no-cache-dir -r requirements.txt

CMD ["python3", "./main.py"]
