FROM python:3.7.2

ARG DEBUG

RUN apt update
RUN apt install -y python3-venv

WORKDIR /home/python/app
ADD . /home/python/app

RUN useradd -ms /bin/bash python
USER python

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
