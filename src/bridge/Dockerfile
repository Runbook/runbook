######################################
### Runbook.io - Bridge Dockerfile ###
######################################


# Pull base image
FROM ubuntu:14.04

# Update
RUN apt-get update --fix-missing
RUN apt-get upgrade -y

# Install python
RUN apt-get install -y python python-dev python-pip python-virtualenv wget unzip
RUN rm -rf /var/lib/apt/lists/*


# Create working directory
RUN mkdir -p /code /config
ADD requirements.txt /config/requirements.txt
ADD config/config.yml /config/config.yml

# Install requirements
RUN pip install -r /config/requirements.txt

CMD python /code/mgmtscripts/create_db.py /config/config.yml && \
    python /code/bridge.py /config/config.yml
