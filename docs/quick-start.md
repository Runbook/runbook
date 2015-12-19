# Quick Start

In this guide we will walk through the steps to deploy Runbook within a Docker container. With this setup all of the Runbook components will be deployed within a single container.

In order to deploy Runbook in a highly available and distributed fashion you can reference our [Basic Install](install.md) and [Deploy with Docker Compose](install_docker_compose.md) guides.

Deployment of a single self hosted instance of Runbook can be performed in 3 steps with Docker.

## Deploy a RethinkDB instance

```sh
$ docker run -d --name rethinkdb rethinkdb
```

## Deploy a Redis instance

```sh
$ docker run -d --name redis redis
```

## Deploy a Runbook instance

```sh
$ docker run -d --name runbook -p 8000:8000 --link rethinkdb:rethinkdb --link redis:redis runbook/runbook
```

Once launched simply navigate to `https://<serverip>:8000`.

---
