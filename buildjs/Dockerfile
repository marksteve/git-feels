FROM ubuntu:trusty

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update

RUN apt-get -y install software-properties-common
RUN add-apt-repository -y ppa:chris-lea/node.js
RUN apt-get update
RUN apt-get -y install nodejs
RUN apt-get -y install git
RUN npm install -g browserify
RUN npm install -g watchify
RUN npm install reactify
RUN npm install uglifyify

WORKDIR /devcup
CMD ["buildjs/buildjs.sh"]
