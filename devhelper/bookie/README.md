

# Installing bookie

Run either:
```
make install
```

or:
```
make develop
```

The latter is useful if you're poking with the source code


# Testing bookie

After running:
```
cd tests
bookie reaction reaction_example.yml
```

Check the generated files under `tests/src`, namely:
```
src/web/reactionforms/pagerduty-notification/__init__.py
src/web/templates/reactions/pagerduty-notification.html
src/actions/actions/pagerduty-notification/__init__.py
```

## About call_on

Currently the `call_on` attribute needs to be completely specified in the yaml model file.

This will generate the model file `src/web/reactionforms/<reaction>/__init__.py` with the full specification of `call_on`.

The view file `src/web/templates/reactions/<reaction>.html` will only contain the include call for `call_on`, namely:
```
            {% include 'reactions/callon.html' %}
```


# Cleaning install files

```
make clean
```
