FROM ubuntu:trusty
ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get -y install software-properties-common
RUN apt-get -y install build-essential
RUN apt-get -y install python-dev
RUN apt-get -y install python-setuptools
RUN easy_install -U pip

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

WORKDIR /devcup
CMD ["python", "manage.py", "runserver"]

