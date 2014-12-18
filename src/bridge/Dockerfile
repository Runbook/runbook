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

ADD requirements.txt /config/requirements.txt

RUN \
  pip install -r /config/requirements.txt
