# Install Guide! (alpha)

## Basics

1. Clone the repo
1. Create and activate a virtualenv
1. Install the requirments - `sh build.sh`

## Config Settings

Update the variables with the string "update_me!" in the `instance/crweb_sample.cfg` file then rename the file to `crweb.cfg`.

> **NOTE**: If you're just getting started, there's no need to update the variables. Just rename the file and then move on. Update the variables as necessary in the future.

## rethinkDB Settings

We use [rethinkDB](http://www.rethinkdb.com/) for persistence. New to rethink? [Install](http://www.rethinkdb.com/docs/install/), then check out the [Quickstart](http://www.rethinkdb.com/docs/quickstart/).

> **NOTE**: Make sure the version of rethinkDB matches the rethinkDB driver version, which you can find in the `requirements.txt` file.

Once installed, create the database from the Python shell:

```sh
>>> import rethinkdb as r
>>> conn = r.connect( "localhost", 28015).repl()
>>> r.db_create('crdb').run(conn)
```

Next, start the server in a new terminal window:

```sh
$ rethinkdb
```

Finally, let's set the authentication key, which you can find in the `instance/crweb_sample.cfg` file:

```sh
$ rethinkdb admin --join localhost:29015
localhost:29015> set auth <auth_key>
```

Boom!

## Redis Settings

Need to show!

## Test

```sh
$ python src/crweb/web.py
```
