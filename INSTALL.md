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

Then with the server running, run the following in a new window to set the authentication key (which comes from "/src/crweb/instance/crweb.cfg.default"):

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

 - crweb/instance/crweb.cfg.default - used by Web (crweb/web.py) process
 - cram/config/control.yml.5min.default - used by cram/control.py process
 - cram/config/main.yml.default - used by cram/broker.py and cram/worker.py processes
 - crbridge/config/config.yml.default - used by crbridge/bridge.py, crbridge/broker.py and crbridge/actioner.py processes

### Initialize database

There is a `create_db.py` script for initializing RethinkDB. Create the database and required tables from the Python shell:

```sh
$ python create_db.py src/crweb/instance/crweb.cfg.default
```

### Running for the first time

With rethinkDB and redis running...

1) Run web processes (src/crweb/web.py)

```sh
$ python src/crweb/web.py instance/crweb.cfg.default
```

2) Run control process (src/cram/control.py)

```sh
$ python src/cram/control.py config/control.yml.5min.default
```

3) Run broker and worker (src/cram/broker.py and src/cram/worker.py)

```sh
$ python src/cram/broker.py config/main.yml.default
$ python src/cram/worker.py config/main.yml.default
```

4) Run bridge, broker, and actioner (src/crbridge/bridge.py, src/crbridge/broker.py, src/crbridge/acrioner.py)

```sh
$ python src/crbridge/bridge.py config/config.yml.default
$ python src/crbridge/broker.py config/config.yml.default
$ python src/crbridge/actioner.py config/config.yml.default
```

Now you can launch your browser and point it to `http://localhost:8000/signup`. Signup, create a monitor and a reaction, watch them being executed.

### Run Tests

Without coverage:

```sh
$ python src/crweb/tests.py
```

With coverage:

```sh
$ python src/crweb/cov.py
```

> Tests only cover "src/crweb" right now.

## Once everything is working fine

You can now use these 3 tmux scripts which run databases and other 7 processes with default settings with panes splitted.*You should have [tmux](http://tmux.sourceforge.net) installed for these to work.*

Run databases and web:

```sh
$ ./tmux_1_web_and_databases.sh
```

Run all cram processes:

```sh
$ ./tmux_2_cram.sh
```

Run all crbridge processes:

```sh
$ ./tmux_3_crbridge.sh
```
