# Docker Setup

This guide will walk you through installing and launching of Runbook with Docker and Fig. The benefit of this setup vs. the normal installation is once setup, you can quickly setup and destroy an isolated Runbook environment as needed with only a few commands.

## Docker with Fig

While each application component has a Dockerfile, for ease of deployment we utilize Fig to start and stop Docker containers.

### Install Docker

Start by [installing](https://docs.docker.com/installation/) Docker version 1.3 or greater. If you're on OSX, use the [OSX Installer](https://docs.docker.com/installation/mac/) to get both Docker and boot2docker. You should now have boot2docker running. If not, run the following commands after install:

```sh
$ boot2docker init
$ boot2docker start
$ (boot2docker shellinit)
```

This should return the `DOCKER_HOST` environment variables, which should look something like this:


```sh
To connect the Docker client to the Docker daemon, please set:
    export DOCKER_HOST=tcp://192.168.59.103:2376
    export DOCKER_CERT_PATH=/Users/michaelherman/.boot2docker/certs/boot2docker-vm
    export DOCKER_TLS_VERIFY=1
```

Copy and paste them directly in your terminal to set the variables. *Optional: To make these stick (so they load each time you open your terminal), add them to your bash profile.*

### Install Fig

```sh
$ curl -L https://github.com/docker/fig/releases/download/1.0.1/fig-`uname -s`-`uname -m` > /usr/local/bin/fig; chmod +x /usr/local/bin/fig
```

## Functionality

Now that Docker and Fig are installed we can use Fig to launch and manage the containers. All fig commands must be run from the same directory the `fig.yml` file is in. In our case this is the main directory, `cloudroutes-service`.

### Starting up the environment with Fig

```sh
$ fig up -d
```

During boot the `bridge` container will run `src/bridge/mgmtscripts/create_db.py` which will connect to RethinkDB and create the required database structure.

### Stopping Fig

Run the following command to stop all servies:

```sh
$ fig stop
```

Then run `fig up -d` to start back up.

### Reading logs/output

To review logs or container output you can use the `logs` option with fig.

```sh
$ fig logs
```

### Resetting

Sometimes during development you may want to clear the database or wipe active containers. To do this simply run the following commands.

```sh
$ fig kill
$ fig rm
```

## Accessing the Web Application

To access the web application you can simply enter the IP of the vm into your browser targeting port 8080 - i.e., [http://192.168.33.10:8080](http://192.168.33.10:8080)

You can find the vm's IP with:

```sh
$ boot2docker ip
```
