# Docker Setup

This guide will walk you through installing and launching of Runbook with [Docker](https://www.docker.com/), [Docker Machine](https://docs.docker.com/machine/), and [Docker Compose](https://docs.docker.com/compose/). The benefit of this setup vs. the normal installation is once setup, you can quickly setup and destroy an isolated Runbook environment as needed with only a few commands.

*While each application component has a Dockerfile, for ease of deployment we utilize Docker Machine and Compose to start, stop, and link Docker containers.*

Before you start, make sure you cloned the [repo](https://github.com/asm-products/cloudroutes-service) and then navigate to the local project directory.

## Install Docker Machine

Start by [installing](https://docs.docker.com/machine/#installation) Docker Machine (v0.2.0 as of writing), which installs Docker as well. Once done, test the install:

```sh
$ docker-machine --v
docker-machine version 0.2.0 (8b9eaf2)
```

Now start a new Machine and point Docker at it:

```sh
$ docker-machine create -d virtualbox runbook-dev;
$ eval "$(docker-machine env runbook-dev)"
```

You can view your currently running machines like so:

```sh
$ docker-machine ls
NAME          ACTIVE   DRIVER         STATE     URL                         SWARM
runbook-dev   *        virtualbox     Running   tcp://192.168.99.100:2376
Michaels-MacBook-Pro-3:cloudroutes-service michael$
```

Make sure the new machine is active. If not, run - `docker-machine active runbook-dev`

## Install Docker Compose

[Install](http://docs.docker.com/compose/install/) Docker Compose (v1.2.0 as of writing).

Again, test the install:

```sh
$ docker-compose --version
docker-compose 1.2.0
```

## Functionality

Now that Docker Machine and Compose are installed we can use Compose to launch, sync, and manage the containers. All Compose commands must be run from the same directory that the *docker-compose.yml* file is in. In our case this is the main (or root) directory, `cloudroutes-service`.

### Starting up the environment with Fig

```sh
$ docker-compose build
$ docker-compose up -d
```

During boot the `bridge` container will run `src/bridge/mgmtscripts/create_db.py` which will connect to RethinkDB and create the required database structure.

### Stopping Fig

Run the following command to stop all servies:

```sh
$ docker-compose stop
```

Then run `docker-compose up -d` to start back up.

### Reading logs/output

To review logs or container output you can use the `logs` option with fig.

```sh
$ docker-compose logs
```

### Resetting

Sometimes during development you may want to clear the database or wipe active containers. To do this simply run the following commands.

```sh
$ docker-compose kill
$ docker-compose rm
```

## Accessing the Web Application

To access the web application you can simply enter the IP of the vm into your browser targeting port 8000 - i.e., [http://192.168.33.10](http://192.168.33.10)

You can find the vm's IP with:

```sh
$ docker-compose ip
```