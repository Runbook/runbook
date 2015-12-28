# Introduction

Runbook is designed to keep the creation of Monitors and Reactions as simple as possible by making everything modular. In order to create a new Reaction you do not have to touch any existing code. Instead, you simply create several new files that are dynamically loaded by the application.

## Defining a "short-name"

Before creating a new reaction, it is important to first define a **short-name** for the reaction. This short-name will be used to identify the Reaction throughout the various components of Runbook. The short-name will be used as a module name for the `actions` component and in the URL for the `web` component. Since this name is used within the URL for the Runbook web interface it is important to select a "web-safe" name.

Currently reactions follow a convention of all lowercase with words separated by a `-` (e.g. `execute-shell-command`, `cloudflare-dns-failover`).

# Creating a new Reaction

## Step 1: Reaction web form

The first step in creating a new reaction is to define a web form. This web form will be used by end users to create their reaction, as such the form should have fields for all of the information required to perform the reaction's action.

Runbook's web interface is written using the [Flask](http://flask.pocoo.org/) framework and all web forms within the web application are created with [wtforms](https://wtforms.readthedocs.org/en/latest/). Familiarity with these two components will help in the development of the web form but are not required.

Creating a new reaction web form is as simple as creating a new directory within `src/web/reactionforms` and creating an `__init__.py` file within that new directory.

    $ mkdir src/web/reactionforms/some-reaction
    $ vi src/web/reactionforms/some-reaction/__init__.py

Once the file exists simply start by creating a new **wtforms** form with a class name of `ReactForm`. Below is an example of the `execute-shell-command` reaction's web form.

```
from wtforms import SelectField, TextAreaField, TextField
from wtforms.validators import DataRequired, Optional
from ..base import BaseReactForm


class ReactForm(BaseReactForm):

    ''' Class that creates an form for the reaction Execute Shell Command '''
    title = "Execute Shell Command"
    description = """
    <p>This reaction provides a method of executing an arbitrary shell command, script or series of commands on a remote host over SSH.</p>
    <p>The SSH connection is authenticated by an SSH key; it is recommended that you generate a unique SSH public/private key pair for this purpose. The <code>Gateway</code> field can be used to specify a bastion or "jump" host; this setting will cause the reaction to first SSH to the specified <code>Gateway</code> host and then SSH to the specified target host.</p>
    """
    placeholders = BaseReactForm.placeholders
    field_descriptions = BaseReactForm.descriptions

    host_string = TextField(
        "Target Host",
        description=field_descriptions['ssh']['host_string'],
        validators=[DataRequired(message='Target Host is a required field')])
    gateway = TextField(
        "Gateway Host",
        description=field_descriptions['ssh']['gateway'],
        validators=[Optional()])
    username = TextField(
        "Username",
        description=field_descriptions['ssh']['username'],
        validators=[DataRequired(message="Username is a required field")])
    sshkey = TextAreaField(
        "SSH Private Key",
        description=field_descriptions['ssh']['sshkey'],
        validators=[DataRequired(message='SSH Key is a required field')])
    cmd = TextAreaField(
        "Command",
        description=field_descriptions['ssh']['cmd'],
        validators=[DataRequired(message='Command is a required field')])
    call_on = SelectField(
        'Call On',
        description=field_descriptions['callon'],
        choices=[('false', 'False Monitors'), ('true', 'True Monitors')],
        validators=[DataRequired(message='Call on is a required field.')])
```

In the code above the `ReactForm` class inherits the `BaseReactForm` class. This is important as this base class creates several basic form fields such as `name`, `trigger`, and `frequency`. The base class also contains a `placeholders` object and `field_descriptions` object which is used for form rendering.

The `placeholders` object defines placeholder text to be shown when the web form renders. This text is selected based on the forms name. Within the `src/web/reactionforms/base.py` file there exists a set of base placeholder values. When creating a custom reaction you can append new values or update existing values using `placeholders.update({ 'newfield' : 'placeholder text'})` within the custom reaction. If the placeholder being created will be reused often than it is best to place this new definition in the `src/web/reactionforms/base.py` file.

The `field_descriptions` object defines help text to be shown as a popover when the web form renders. Like the `placeholders` object this is populated from the `src/web/reactionforms/base.py` module. Common descriptions already exist such as the ones shown above, however when creating a new reaction you can either update the object or for each field specify a description manually. Either option is accepted however do try to follow the DRY (Don't Repeat Yourself) methodology as much as possible.

In addition to field descriptions the `ReactForm` class also requires a `description` and `title` to be defined. These are used during page rendering to provide users with information on how a reaction works and is to be used. Our overall documentation does not document each and every reaction as the `description` is the place for that functionality. The `description` object is the only one at this time designated as HTML Safe. HTML should only be used with the `description` object.

## Step 2: Reaction module


Once a web form has been created the next task is to create the reaction module itself. Reaction modules contain the logic for performing the reaction. These modules exist within the `src/actions/actions/` directory. To create a new one the first step is similar to the web form, simply create a new directory and within that directory a `__init__.py` file.

    $ mkdir src/actions/actions/some-reaction
    $ vi src/actions/actions/some-reaction/__init__.py

When the reaction actioner process (`src/actions/actioner.py`) receives a request to perform a reaction action it will import the `action()` method from the `src/actions/action/<short-name>` module. As such all reactions require a `action()` method to be defined. This method will be called with `kwargs` of `jdata`, `redata`, `rdb`, `r_server`, `config` and `logger`.

The `rdb` object is a object for interacting with RethinkDB, `r_server` is used for interacting with the Redis cache and `logger` is for writing logs.

### Sample `redata` Object

The below is an example of the `redata` object. This object is used to contain information about the reaction being executed. The data is essentially the full database contents of the specific reaction.

    redata = {
      "data": {
        "apikey":  "dslfjalskdj32432lajfs233432fcaewrq11c",
        "domain":  "example.com",
        "email": "example@example.com",
        "ip":  "10.0.3.1",
        "name":  "Remove: example.com - 10.0.3.1"
      } ,
      "frequency": 0,
      "id":  "kasdkldj2342-23faew-234fs-a39d519f78",
      "lastrun": 1411916840.440264,
      "name":  "Remove: example.com - 10.0.3.1",
      "rtype":  "cloudflare-ip-remove",
      "trigger": 0,
      "uid":  "kasldflksajl-asfw-1337-1337-asdfa213"
    }


### Sample `jdata` Object

The below `jdata` object is essentially the same as the `jdata` object used for monitors. This object contains the monitor specific information pulled from the database. However, the `actioner.py` process does pull some additional data from the database that the monitor processes do not receive.

    jdata = {
      "status": "false",
      "uid": "1232131231231231231-111-15888dd98382",
      "zone": "Digital Ocean - sfo1",
      "cid": "232132312312312313123-aea-qer2-vs4e3",
      "url": "Twerewu230432423owrjewoj3fw3r-.2342432fserw323eaew1234567890204zT6el98CmmI2X30SwCo",
      "ctype": "http-keyword",
      "failcount": "412",
      "time_tracking": {
        "control": 1411488928.422103,
        "ez_key": "key@example.com",
        "env": "Prod"
      },
      "check": {
        "status": "true",
        "prev_status": "true",
        "method": "automatic"
      },
      "cacheonly": False,
      "data": {
        "regex": "True",
        "datacenter": [
          "dc2queue",
          "dc1queue"
        ],
        "name": "Some Monitor",
        "keyword": "Test",
        "reactions": [
          "1232432jsad-aefawewr2-adsfa-q23261c5",
          "asfkldjsafj0eq2.-23rq23=afsedfadc359"
        ],
        "url": "http://example.com/hello.txt",
        "timer": "5mincheck",
        "host": "example.com",
        "present": "True"
      },
      "name": "Some Monitor"
    }

For both the `jdata` and `redata` objects the `data` key contains user supplied information to be used during the reaction process.

### Example Module

The below is an example reaction module based on the `execute-shell-command` reaction.

```
from fabric.api import env, run, hide
from ..utils import ShouldRun

def __action(**kwargs):
    redata = kwargs['redata']
    jdata = kwargs['jdata']
    if ShouldRun(redata, jdata):
        env.gateway = redata['data']['gateway']
        env.host_string = redata['data']['host_string']
        env.user = redata['data']['username']
        env.key = redata['data']['sshkey']
        env.disable_known_hosts = True
        env.warn_only = True
        env.aport_on_prompts = True
        try:
            results = run_cmd(redata['data']['cmd'])
            if results.succeeded:
                return True
            else:
                raise Exception(
                    'Command Execution Failed: {0} - {1}'.format(results.return_code, results))
        except:
            raise Exception(
                'Command failed to execute')
    else:
        return None  

def run_cmd(cmd):
    with hide('output', 'warnings'):
        return run(cmd, timeout=1200)


def action(**kwargs):
    try:
        return __action(**kwargs)
    except Exception, e:  #pylint: disable=broad-except
        redata = kwargs['redata']
        logger = kwargs['logger']
        logger.warning(
            'execute-shell-command: Reaction {id} failed: {message}'.format(
                id=redata['id'], message=e.message))
        return False
```

#### ShouldRun

Reactions are called after every monitor check, it is up to each individual reaction to determine if it should actually perform the action or not. In order to make this easier you can simply import the `ShouldRun` method from the `..utils` module. This method will identify if the reaction should actually be executed or not. If we look at the code above we can see that all of the execution steps are within an `if ShouldRun(redata, jdata):` statement.

After a successful execution the reaction should return a `True` value. If the reaction is unable to execute because of an error the return value should be `False`. The `None` return value is used to specify that the reaction was not executed for expected reasons such as the `ShouldRun()` method returning `False`.

## Step 3: Enabling the reaction

By default any reaction that exists within the `reactionforms/` directory can be accessed via the Web UI. Available reactions are defined within the `src/web/instance/reactions.cfg` file. This file contains a Python dictionary with the defined reactions. To enable a reaction simply append the appropriate details within this configuration file.

Below is an example of the Slack Webhook Reaction.

```
    'Chat Services' : {
        'Slack Webhooks' : {
            'description' : 'The Slack Webhooks Reaction allows you to integrate Runbook monitors with Slack. This reaction uses Slacks incoming webhooks to post to channels or users.',
            'create_link' : '/dashboard/reactions/slack-webhook',
            'service' : 'Slack',
        },
    },
```

# Getting help

If you need help while developing a new reaction or modifying an existing reaction you can find help on Runbook's [Gitter Chat](https://gitter.im/Runbook/runbook). For a list of reactions to be created checkout our [Waffle.io Board](https://waffle.io/Runbook/runbook).
