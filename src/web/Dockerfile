#######################################
### Runbook.io - Web App Dockerfile ###
#######################################


# Pull base image
FROM ubuntu:14.04

# Update
RUN apt-get update --fix-missing
RUN apt-get upgrade -y

# Install python
RUN apt-get install -y python python-dev python-pip python-virtualenv wget unzip build-essential libssl-dev libffi-dev
RUN rm -rf /var/lib/apt/lists/*


# Create working directory
RUN mkdir -p /code/instance /config
ADD requirements.txt /config/requirements.txt
ADD instance/web.cfg /config/web.cfg
# Install requirements
RUN pip install -r /config/requirements.txt

CMD python /code/web.py /config/web.cfg 
