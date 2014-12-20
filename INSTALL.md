## First Time Setup

### Basics

1. Clone the repo
1. Create and activate a virtualenv
1. Install the requirements - `sh build.sh`

### RethinkDB Setup

We use [rethinkDB](http://www.rethinkdb.com/) for persistence. New to rethink? [Install](http://www.rethinkdb.com/docs/install/), then check out the [QuickStart](http://www.rethinkdb.com/docs/quickstart/).

*Make sure to follow these rules regarding the server vs. driver versions:*

- IF driver < 1.13 THEN use server < 1.13
- IF driver >= 1.13 THEN use server > 1.13

Once installed, start the server in a new terminal window:

```sh
$ rethinkdb
```

Then with the server running, run the following in a new window to set the authentication key (which comes from "/src/web/instance/web.cfg.default"):

```sh
$ rethinkdb admin set auth cloudroutes
```

### Redis Setup

Download [Redis](http://redis.io/download) (if necessary), then fire up the server in a new terminal window:

```sh
$ redis-server
```

### Configuration

The entire application has 4 configuration file types, which are used by 7 types of processes. This is because having different processes of the same type requires different configurations (ports, data shards, etc.). A minimal application will have exactly 7 processes and 4 configuration files.

Here is a list of configuration files, that can be used for the first time to run a minimal working application locally:

 - web/instance/web.cfg.default - used by Web (web/web.py) process
 - monitors/config/control.yml.5min.default - used by monitors/control.py process
 - monitors/config/main.yml.default - used by monitors/broker.py and monitors/worker.py processes
 - bridge/config/config.yml.default - used by bridge/bridge.py processes
 - actions/config/config.yml.default - used by actions/broker.py and actions/actioner.py processes

### Initialize database

There is a `create_db.py` script for initializing RethinkDB. Create the database and required tables from the Python shell:

```sh
$ python src/bridge/mgmtscripts/create_db.py src/bridge/config/config.yml.default
```

### Run all processes

```
$ foreman start
```

Now you can launch your browser and point it to http://localhost:8000/signup. Signup, create a monitor and a reaction, and then watch them execute.

### Run Tests

Without coverage:

```sh
$ python src/web/tests.py
```

With coverage:

```sh
$ python src/web/cov.py
```

> Tests only cover "src/web" right now.