#
# Runbook.io - Web App Dockerfile
#

# Pull base image.
FROM dockerfile/ubuntu

# Install Python.
RUN \
  apt-get update && \
  apt-get install -y python python-dev python-pip python-virtualenv wget unzip && \
  rm -rf /var/lib/apt/lists/*

RUN \
  mkdir -p /code /config

ADD requirements.txt /code/requirements.txt

RUN \
  pip install -r /code/requirements.txt

EXPOSE 6000
EXPOSE 6001
