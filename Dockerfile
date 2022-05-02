FROM python:3.9.9-slim-buster

COPY ./requirements.txt /requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /code

WORKDIR /code
