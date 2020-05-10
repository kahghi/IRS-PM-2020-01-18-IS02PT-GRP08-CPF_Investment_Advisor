FROM python:3-onbuild

FROM ubuntu:18.04

RUN sudo apt install unixodbc-dev

RUN yum install unixODBC-devel

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

CMD [ "uwsgi", "app.ini" ]