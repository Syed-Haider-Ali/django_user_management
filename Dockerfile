FROM python:3.10

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=authentication.settings

WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

