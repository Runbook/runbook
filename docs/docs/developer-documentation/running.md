# Installation Guide

This installation guide will help you with your initial setup of [Runbook](https://runbook.io).

---

## Easy setup route

Some steps provide easy setup default values, which you may want to use if doing a first-time setup to speed things up. Using easy setup options leads you through an installation happy path (easy setup route). Such options are marked as **_(EASY)_**.


## Basics

1. Clone the repo
1. Create and activate a virtualenv
1. Install the requirements: `sh build.sh`

## RethinkDB setup

We use [RethinkDB](http://www.rethinkdb.com/) for persistence. New to RethinkDB? [Install](http://www.rethinkdb.com/docs/install/), then check out the [quickstart](http://www.rethinkdb.com/docs/quickstart/).

*Make sure to follow these rules regarding the server vs. driver versions:*

- IF driver < 1.13 THEN use server < 1.13
- IF driver >= 1.13 THEN use server > 1.13

Once installed, start the server in a new terminal window:

```sh
$ rethinkdb
```

Choose authentication key for RethinkDB and set it:

```sh
$ rethinkdb admin --join localhost:29015
localhost:29015> set auth <auth_key>
```

**_(EASY)_** you may want to choose `cloudroutes` key, which will match to what is set in `*.default` configuration files:

```sh
$ rethinkdb admin set auth cloudroutes
```


## Redis setup

Download [Redis](http://redis.io/download) (if necessary), then fire up the server in a new terminal window:

```sh
$ redis-server
```


## Configuration

An application has 4 configuration file types, which are used by 7 types of processes. This is because having different processes of the same type requires different configurations (ports, data shards, etc.). A minimal application will have exactly 7 processes and 4 configuration files.

**_(EASY)_** Here is a list of configuration files, that can be used for the first time to run a minimal working application locally:

 - crweb/instance/crweb.cfg.default - used by Web (crweb/web.py) process
 - cram/config/control.yml.5min.default - used by cram/control.py process
 - cram/config/main.yml.default - used by cram/broker.py and cram/worker.py processes
 - crbridge/config/config.yml.default - used by crbridge/bridge.py, crbridge/broker.py and crbridge/actioner.py processes


## Initialize the database

There is a `create_db.py` script for initializing RethinkDB.

**_(EASY)_** Create the database and required tables from the Python shell:

```sh
$ python create_db.py src/crweb/instance/crweb.cfg.default
```


## Running for the first time

1) Run web processes (src/crweb/web.py)

**_(EASY)_** run web:

```sh
$ python src/crweb/web.py instance/crweb.cfg.default
```

2) Run control process (src/cram/control.py)

**_(EASY)_** run control:

```sh
$ python src/cram/control.py config/control.yml.5min.default
```

3) Run broker and worker (src/cram/broker.py and src/cram/worker.py)

**_(EASY)_** run broker:

```sh
$ python src/cram/broker.py config/main.yml.default
```

**_(EASY)_** run worker:

```sh
$ python src/cram/worker.py config/main.yml.default
```

4) Run bridge, broker, and actioner (src/crbridge/bridge.py, src/crbridge/broker.py, src/crbridge/acrioner.py)

**_(EASY)_** run bridge:

```sh
$ python src/crbridge/bridge.py config/config.yml.default
```

**_(EASY)_** run broker:

```sh
$ python src/crbridge/broker.py config/config.yml.default
```

**_(EASY)_** run actioner:

```sh
$ python src/crbridge/actioner.py config/config.yml.default
```

Now you can launch your browser and point it to `http://localhost:8000/signup`. Sign up, create a monitor and a reaction, and watch them being executed.


## Note: Relative vs absolute URLs

When deployed in production, static pages such as `/`, `/pages/tos`, and `/pages/pricing` are prefetched and saved as HTML files. Since the static pages in production are `https://runbook.io` and the web app runs as `https://dash.runbook.io`, the **login** and **signup** links are always absolute URLs. All other links should be kept as relative URLs. To get started with your local instance, simply point your browser to `http://localhost:8000/signup`


## Run tests

```sh
$ python src/crweb/tests.py
```


## Once everything is working correctly

You can now use these 3 tmux scripts which run databases and other 7 processes with default settings with panes split.

**_(EASY)_** yes, these scripts only work if you follow the easy setup route

You should have [tmux](http://tmux.sourceforge.net) installed for these to work.

run databases and web:

```sh
$ ./tmux_1_web_and_databases.sh
```

run all cram processes:

```sh
$ ./tmux_2_cram.sh
```

run all crbridge processes:

```sh
$ ./tmux_3_crbridge.sh
```

---