## Prerequisites

Runbook utilizes RethinkDB and Redis for data persistence, and several Python modules for communications and functionality. Before launching Runbook you will need to install several prerequisites.

### RethinkDB Setup

We use [rethinkDB](http://www.rethinkdb.com/) for persistence. New to rethink? [Install](http://www.rethinkdb.com/docs/install/), then check out the [QuickStart](http://www.rethinkdb.com/docs/quickstart/).

*Make sure to follow these rules regarding the server vs. driver versions:*

- IF driver < 1.13 THEN use server < 1.13
- IF driver >= 1.13 THEN use server > 1.13

Need to check your version?

```sh
$ rethinkdb --version
rethinkdb 1.16.2-1 (CLANG 6.0 (clang-600.0.56))
```

Once installed, start the server in a new terminal window:

```sh
$ rethinkdb
```

Then with the server running, run the following script to set the authentication key:

```sh
$ python src/bridge/mgmtscripts/set_rethink_auth_key.py
```

### Redis Setup

Download [Redis](http://redis.io/download) (if necessary), then fire up the server in a new terminal window:

```sh
$ redis-server
```

### Python Module Installation

Install required Python modules using `pip`.

```
$ sudo pip install -r src/web/requirements.txt
$ sudo pip install -r src/bridge/requirements.txt
$ sudo pip install -r src/monitors/requirements.txt
$ sudo pip install -r src/actions/requirements.txt
```

## Launching Runbook

### Configuration

Runbook consists of 7 components (**Web**, **Bridge**, **Control**, **Monitor Broker**, **Monitor Worker**, **Action Broker**, **Actioner**); these components are located within 4 main sections `src/web`, `src/monitors`, `src/bridge`, and `src/actions`.

Below is a list of configuration files, that can be used to launch a basic Runbook instance.

 - `src/web/instance/web.cfg` - used by **Web**
 - `src/bridge/config.yml` - used by **Bridge**
 - `src/monitors/config/control-<time>.yml` - used by **Control**
 - `src/monitors/config/broker.yml` - used by **Monitor Broker**
 - `src/monitors/config/worker.yml` - used by **Monitor Worker**
 - `src/actions/config/broker.yml` - used by **Action Broker**
 - `src/actions/config/actioner.yml` - used by **Actioner**

### Initialize database

In order to initialize (creating db and tables) RethinkDB there is a `create_db.py` script located at `src/bridge/mgmscripts/create_db.py`.

Create the database and required tables:

```sh
$ python src/bridge/mgmtscripts/create_db.py src/bridge/config/config.yml.default
```

### Run all processes

The top-level repository directory contains a `Procfile`, use any `Procfile` compatible process launcher.

```
$ foreman start
```

Alternatively, if you wish to launch each component without `foreman` you can simply use the commands specified in the `Procfile`.

Now you can launch your browser and point it to http://localhost:8000.
