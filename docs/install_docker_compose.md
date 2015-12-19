## Docker Setup

This guide will walk you through installing and launching of Runbook with [Docker](https://www.docker.com/), [Docker Machine](https://docs.docker.com/machine/), and [Docker Compose](https://docs.docker.com/compose/). The benefit of this setup is that it could be used for Development and Production environments.

*While each application component has a Dockerfile, for ease of deployment we utilize Docker Machine and Compose to start, stop, and link Docker containers.*

Before you start, clone the [Runbook GitHub Repository](https://github.com/Runbook/runbook) and then navigate to the local project directory.

### Install Docker Machine

Start by [installing](https://docs.docker.com/machine/#installation) Docker Machine, which installs Docker Engine as well. Once done, test the install:

```sh
$ docker-machine --v
docker-machine version 0.2.0 (8b9eaf2)
```

Now start a new Machine and point Docker at it:

```sh
$ docker-machine create -d virtualbox runbook-dev;
$ eval "$(docker-machine env runbook-dev)"
```

In order to view currently running machines use the `docker-machine` command with the `ls` option:

```sh
$ docker-machine ls
NAME          ACTIVE   DRIVER         STATE     URL                         SWARM
runbook-dev   *        virtualbox     Running   tcp://192.168.99.100:2376
```

Before continuing make sure machines are active. If not, execute `docker-machine active runbook-dev`.

### Install Docker Compose

First, [install](http://docs.docker.com/compose/install/) Docker Compose.

```sh
$ docker-compose --version
docker-compose 1.2.0
```

## Deployment

Now that Docker Machine and Compose are installed we can use Compose to launch, sync, and manage the containers. All Compose commands must be run from the same directory that the `docker-compose.yml` file is in. In our case this is the main (or root) project director.

### Building images

```sh
$ docker-compose build
```

### Starting up containers

```sh
$ docker-compose up -d
```

During boot the `bridge` container will execute `/code/mgmtscripts/create_db.py` which will connect to RethinkDB and create the required database structure.

### Stopping containers

Run the following command to stop all containers:

```sh
$ docker-compose kill
```

Individual containers can be stopped by specifying the container name at the end of the command (I.E. `docker-compose kill web`).

### Reading logs/output

To review logs or container output you can use the `logs` option with compose.

```sh
$ docker-compose logs
```

### Resetting

Sometimes during development you may want to clear the database or wipe active containers. To do this simply run the following commands.

```sh
$ docker-compose kill
$ docker-compose rm
$ docker-compose build
$ docker-compose up -d
```

## Accessing the Web Application

To access the web application you can simply enter the IP of the running machines into your browser such as http://192.168.33.10.

You can find machine IP's with:

```sh
$ docker-compose ip
```

