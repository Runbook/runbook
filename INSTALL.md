# Install Guide!

Welcome!

## Basics

1. Clone the repo
1. Create and activate a virtualenv
1. Install the requirements - `sh build.sh`

## Config Settings

Update the variables with the string "update_me!" in the `instance/crweb_sample.cfg` file then rename the file to `crweb.cfg`.

> **NOTE**: If you're just getting started, there's no need to update the variables. Just rename the file and then move on. Update the variables as necessary in the future.

## rethinkDB Setup

We use [rethinkDB](http://www.rethinkdb.com/) for persistence. New to rethink? [Install](http://www.rethinkdb.com/docs/install/), then check out the [QuickStart](http://www.rethinkdb.com/docs/quickstart/).

*Make sure to follow these rules regarding the server  vs. driver versions:*

- IF driver < 1.13 THEN use server < 1.13
- IF driver >= 1.13 THEN use server > 1.13

Once installed, start the server in a new terminal window:

```sh
$ rethinkdb
```

Create the database and required tables **(before setting authentication)** from the Python shell:

```sh
$ python create_db.py
```

Finally, let's set the authentication key, which you can find in the `instance/crweb.cfg` file:

```sh
$ rethinkdb admin --join localhost:29015
localhost:29015> set auth <auth_key>
```

## Redis Setup

Download [Redis](http://redis.io/download) (if necessary), then fire up the server in a new terminal window:

```sh
$ redis-server
```

## Sanity Check

```sh
$ python src/crweb/web.py
```
