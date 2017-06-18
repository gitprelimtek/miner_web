FROM ubuntu:14.04

MAINTAINER Kaniu Ndungu

WORKDIR /app

RUN  apt-get update

RUN apt-get install -y tar git curl nano wget dialog net-tools build-essential

RUN apt-get install -y python python-dev python-distribute python-pip

RUN  apt-get update

RUN sudo  -H pip install --upgrade pip

ADD requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

#ADD application.py /app/application.py
ADD . /app

EXPOSE 8080

WORKDIR /app

CMD python server.py 

