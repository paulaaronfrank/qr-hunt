# pull official base image
FROM python:3.9.5-slim-buster

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app/

WORKDIR ./src
COPY ./certificate.crt ./certificate.crt
COPY ./private.key ./private.key
CMD ["gunicorn", "--certfile", "./certificate.crt", "--keyfile", "./private.key", "-b", "0.0.0.0:8443", "wsgi:app"]
