# Install Guide! (alpha)

## Basics

1. Clone the repo
1. Create and activate a virtualenv
1. Install the requirments - `sh build.sh`

## Config

1. Update the variables in the `instance/crweb.cfg` file.

## Test

```sh
$ python src/crweb/web.py
```

Current error:

```sh
host=app.config['DBHOST'], port=app.config['DBPORT'],
KeyError: 'DBHOST'
```

Need sample config file!





