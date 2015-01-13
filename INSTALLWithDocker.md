This guide will walk you through installing and launching of Runbook with Vagrant and Docker. The benefit of this setup vs. the normal installation is once setup, you can quickly setup and destroy an isolated Runbook environment as needed with only a few commands.

The Vagrant setup in this guide is optional; however you will need to have an environment that supports both Docker and Fig for the docker setup.

## Vagrant

### Prerequisites

Before starting you must first install:

* [Vagrant](https://docs.vagrantup.com/v2/installation/)
* [Virtualbox](https://www.virtualbox.org/wiki/Downloads)

### Start the vm

Once Vagrant and Virtualbox are installed, you can startup the vm. Run this command from the directory that contains the `Vagrantfile`:

    $ vagrant up

### Logging into the vm

To access the vm you can login with the following command.

    $ vagrant ssh

At this point you have a Vagrant vm that can run the Docker containers. For the next steps you will need to first setup the development environment. To set this up follow the [Quickstart Developer Guide](http://runbook.readthedocs.org/en/develop/developers/) to get the latest code and configurations.

## Docker with Fig

While each application component has a Dockerfile, for ease of deployment we utilize fig to start and stop containers.

### Install Docker

By default the vagrant vm does not have docker installed. To install it use the `apt-get` command.

    $ sudo apt-get install docker.io

### Install Fig

Fig can be installed with python's `pip` package manager. The vagrant vm does not have `pip` installed by default, to do this use the `apt-get` command.

    $ sudo apt-get install python-pip
    $ sudo pip install fig

### Starting up the environment with fig

Now that Docker and Fig are installed we can use Fig to launch and manage the containers. All fig commands must be run from the same directory the `fig.yml` file is in. In our case this is the main directory for the repository.

    $ cd cloudroutes-service
    $ sudo fig up -d

During boot the `bridge` container will run `src/bridge/mgmtscripts/create_db.py` which will connect to RethinkDB and create the required database structure.

#### Reading logs/output

To review logs or container output you can use the `logs` option with fig.

    $ sudo fig logs

#### Resetting

Sometimes during development you may want to clear the database or wipe active containers. To do this simply run the following commands.

    $ sudo fig kill
    $ sudo fig rm

## Accessing the Web Application

To access the web application you can simply enter the IP of the vm into your browser targeting port 8080.

**Example:**

    http://192.168.33.10:8000

### Finding the IP

You can find the vagrant vm's IP via the `ip` command.

    $ ip addr show
