FROM python:3
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code
ADD . /code/
RUN pip install -r requirements/prod.txt
RUN chmod +x docker_entrypoint.sh
RUN apt-get update && apt-get -y install netcat
