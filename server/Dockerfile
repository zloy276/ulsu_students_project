FROM python:3.7.2

ARG DEBUG

USER root

RUN apt update
RUN apt install -y python3-venv
RUN pip3 install poetry

RUN useradd -ms /bin/bash python
USER python

RUN mkdir /home/python/app
WORKDIR /home/python/app

ADD pyproject.toml .
ADD poetry.lock .

RUN if [ "$DEBUG" = "True" ] ; then poetry install ; else poetry install --no-dev ; fi

ADD . /home/python/app

# DEFAULT ENV FOR DATABASE_URL
ENV DATABASE_URL="postgres://postgres@db/postgres"

RUN echo "hello world"