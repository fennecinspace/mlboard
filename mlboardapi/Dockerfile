FROM python:3.8-alpine

# unbUffering output
ENV PYTHONUNBUFFERED 1

# creating workdir
RUN mkdir /code
WORKDIR /code

# dependencies and requirements
ADD requirements.txt /code/
RUN apk add --no-cache gcc build-base libxml2-dev libxslt-dev mariadb-dev gettext \
    && pip install --no-cache-dir -r requirements.txt

ADD . /code/