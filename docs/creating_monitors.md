# Introduction

Runbook is designed to keep the creation of Monitors as simple as possible by making everything modular. In order to create a new Monitor you do not have to touch any existing code. Instead, you simply create several new files that are dynamically loaded by the application.

## Defining a "short-name"

Before creating a new monitor, it is important to first define a **short-name** for the monitor. This short-name will be used to identify the Monitor throughout the various components of Runbook. The short-name will be used as a module name for the `monitors` component and in the URL for the `web` component. Since this name is used within the URL for the Runbook web interface it is important to select a "web-safe" name.

Currently monitors follow a convention of all lowercase with words separated by a `-` (e.g. `execute-shell-command`, `http-request`).

# Creating a new Monitor

## Step 1: Monitor web form

The first step in creating a new monitor is to define a web form. This web form will be used by end users to create the monitor, as such the form should have fields for all of the information required to perform the monitor check.

Runbook's web interface is written using the [Flask](http://flask.pocoo.org/) framework and all web forms within the web application are created with [wtforms](https://wtforms.readthedocs.org/en/latest/). Familiarity with these two components will help in the development of the web form but are not required.

Creating a new monitor web form is as simple as creating a new directory within `src/web/monitorforms` and creating an `__init__.py` file within that new directory.

    $ mkdir src/web/monitorforms/some-monitor
    $ vi src/web/monitorforms/some-monitor/__init__.py

Once the file exists simply start by creating a new **wtforms** form with a class name of `CheckForm`. Below is an example of the `execute-shell-command` monitor's web form.

```
from wtforms import TextField, TextAreaField
from wtforms.validators import DataRequired, Optional
from ..datacenter import DatacenterCheckForm

class CheckForm(DatacenterCheckForm):

    ''' Class that creates an form for the monitor Execute Shell Command '''
    title = "Execute Shell Command"
    description = """
    <p>This monitor provides a method of executing an arbitrary shell command, script or series of commands on a remote host over SSH.</p>
    <p>The SSH connection is authenticated by an SSH key; it is recommended that you generate a unique SSH public/private key pair for this purpose. The <code>Gateway</code> field can be used to specify a bastion or "jump" host; this setting will cause the monitor to first SSH to the specified <code>Gateway</code> host and then SSH to the specified target host.</p>
    <p>Success and Failure are determined by the ability to connect to the remote host, and the exit code provided from the commands executed. An exit code of 0 is a success, and any other exit code is a failure</p>
    """
    placeholders = DatacenterCheckForm.placeholders
    field_descriptions = DatacenterCheckForm.descriptions

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
```

In the code above the `CheckForm` class inherits the `DatacenterCheckForm` class. This is important as this base class creates several basic form fields such as `name`, `reactions`, and `interval`. The base class also contains a `placeholders` object and `field_descriptions` object which is used for form rendering.

The `placeholders` object defines placeholder text to be shown when the web form renders. This text is selected based on the forms name. Within the `src/web/monitorforms/base.py` file there exists a set of base placeholder values. When creating a custom monitor you can append new values or update existing values using `placeholders.update({ 'newfield' : 'placeholder text'})` within the custom monitor. If the placeholder being created will be reused often than it is best to place this new definition in the `src/web/monitorforms/base.py` file.

The `field_descriptions` object defines help text to be shown as a popover when the web form renders. Like the `placeholders` object this is populated from the `src/web/monitorforms/base.py` module. Common descriptions already exist such as the ones shown above, however when creating a new monitor you can either update the object or for each field specify a description manually. Either option is accepted however do try to follow the DRY (Don't Repeat Yourself) methodology as much as possible.

In addition to field descriptions the `CheckForm` class also requires a `description` and `title` to be defined. These are used during page rendering to provide users with information on how a monitor works and is to be used. Our overall documentation does not document each and every monitor as the `description` is the place for that functionality. The `description` object is the only one at this time designated as HTML Safe. HTML should only be used with the `description` object.


## Step 2: Monitor module

Once a web form has been created the next task is to create the monitor module itself. Monitor modules contain the logic for performing the monitor and return either a `True`, `False` or `None` value. These modules exist within the `src/monitors/checks/` directory. To create a new one the first step is similar to the web form, simply create a new directory and within that directory a `__init__.py` file.

    $ mkdir src/monitors/checks/some-monitor
    $ vi src/monitors/checks/some-monitor/__init__.py

When the monitor worker process (`src/monitors/worker.py`) receives a request to perform a monitor check it will import the `check()` method from the `src/monitors/check/<short-name>` module. As such all monitors require a `check()` method to be defined. This method will be called with `kwargs` of `jdata` and `logger`. When called the `check()` method should return `True` for monitors that are True (or healthy), `False` for monitors that are False (or unhealthy) and `None` for monitors that experience and error during execution.

### Example monitor module

The below is the `execute-shell-command` module which is used to execute shell commands over SSH on user systems.

```
from fabric.api import hide, run, env
import time

def run_cmd(cmd):
    with hide('output', 'warnings'):
        return run(cmd, timeout=1200)

def check(**kwargs):
    ''' Login over SSH and execute shell command '''
    jdata = kwargs['jdata']
    logger = kwargs['logger']

    env.gateway = jdata['data']['gateway']
    env.host_string = jdata['data']['host_string']
    env.user = jdata['data']['username']
    env.key = jdata['data']['sshkey']
    env.disable_known_hosts = True
    env.warn_only = True
    env.aport_on_prompts = True
    try:
        results = run_cmd(jdata['data']['cmd'])
        logger.debug("execute-shell-command: requested command" +
                     " returned with exit code {0}".format(results.return_code))
        if results.succeeded:
            return True
        else:
            return False
    except:
        return None
```

In the above we can see that the `jdata` object contains information submitted from the webform within the `data` key. All web form details are saved into `jdata['data']` as a dictionary.

### Example `jdata` object

The `jdata` object is very important as it is used as the source of information for monitors within the monitoring and actioning code. In fact this object is essentially the monitors definition as it is defined within the RethinkDB database. 

Below is an example of what the `jdata` dictionary could contain when the `worker.py` process receives it.

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

As stated above the primary key to utilize when developing a new monitor module is the `jdata['data']` key, as this key holds all user input.

# Step 3: Enabling the monitor

By default any monitor that exists within the `monitorforms/` directory can be accessed via the Web UI. Available monitors are defined within the `src/web/instance/monitors.cfg` file. This file contains a Python dictionary with the defined monitors. To enable the monitor simply append the appropriate details within this configuration file. 

Below is an example of the **Slack Webhook** monitor.

```
  'Chat Services' : {
      'Slack Webhook' : {
            'description' : 'Integrate your Slack channels with Runbook via Slack outgoing webhooks or Slack commands. When calling these monitors from Slack you will receive a response validating that we have recieved it.',
            'create_link' : '/dashboard/monitors/slack-webhook',
      },
  },
```

# Webhook Monitors

Webhook monitors differ quite a bit compared to a non-webhook monitor. At this time this document is out of scope for webhook monitors but a good example can be found within `src/web/monitorforms/slack-webhook` and `src/web/monitorapis/slack-webhook`.

# Getting help

If you need help while developing a new monitor or modifying an existing monitor you can find help on Runbook's [Gitter Chat](https://gitter.im/Runbook/runbook). For a list of monitors to be created checkout our [Waffle.io Board](https://waffle.io/Runbook/runbook).
