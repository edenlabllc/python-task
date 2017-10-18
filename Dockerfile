FROM python:3
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP app.py
ENV FLASK_DEBUG 1
MAINTAINER olha.rysovana@gmail.com

RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
