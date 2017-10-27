FROM python:3.6
EXPOSE 8000
ENV PYTHONUNBUFFERED 1
RUN mkdir /python-task
WORKDIR /python-task
ADD requirements.txt /python-task/
RUN pip install -r requirements.txt
ADD . /python-task/