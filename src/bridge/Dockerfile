######################################
### Runbook.io - Bridge Dockerfile ###
######################################


# Pull base image
FROM dockerfile/ubuntu

# Update
RUN apt-get update
RUN apt-get upgrade -y

# Install python
RUN apt-get install -y python python-dev python-pip python-virtualenv wget unzip
RUN rm -rf /var/lib/apt/lists/*

# Create working directory
RUN mkdir -p /code /config
ADD requirements.txt /config/requirements.txt

# Install requirements
pip install -r /config/requirements.txt