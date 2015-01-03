# Creating Monitors

## Introduction

With Runbook, we have kept the creation of Monitors as simple as possible by making the Monitors modular. Creating a new Monitor doesn't require you to edit the main `web.py` file. Instead, you create several new files that are dynamically loaded into the application.

When creating a new Monitor, it is important to define a **short-name** for the Monitor. This short-name will be used to uniquely identify the Monitor throughout the various modules you create.

**Example:** An HTTP GET-based Monitor that searches for a specific keyword has a short-name of `http-keyword`. This short-name is unique for this type of Monitor and all files created for this Monitor reference the short-name.

In this guide, we will use the `http-keyword` Monitor as a reference. This Monitor is a non Webhook-based Monitor and is a good example of how simple it is to create a Monitor.

## Creating a new Monitor

### Step 1: The Monitor web form

Runbook is written using the [Flask](http://flask.pocoo.org/) framework. A common utility for creating web forms within Flask is [wtforms](https://wtforms.readthedocs.org/en/latest/). We utilize wtforms for all web forms within the Runbook GUI, including the forms that create Monitors.

For this document, we will create a new Monitor named `some-monitor`; the first step of creating a Monitor is to create the web form needed for users. To start the web form we will create a directory in `web/monitorforms/` called `some-monitor`. Within that directory we will create a `__init__.py` file containing a class that defines the required form fields.

    $ mkdir src/web/monitorforms/some-monitor
    $ vi src/web/monitorforms/some-monitor/__init__.py

Within this file is the actual wtforms code. You can use the [http-keyword](https://github.com/asm-products/cloudroutes-service/blob/master/src/web/monitorforms/http-keyword/__init__.py) Monitor as an example.

There are a couple of guidelines when creating a web form for Monitors.

* The class must be named CheckForm

When the main web component loads the form it will dynamically load the CheckForm class. This dynamic loading relies on the short-name and is pulled from the URL the user navigates to.

* The class should inherit either DatacenterCheckForm or BaseCheckForm

When creating a web form the CheckForm should inherit either the BaseCheckForm or the DatacenterCheckForm classes. You can import these classes with the following commands.

**BaseCheckForm**

    from ..base import BaseCheckForm

**DatacenterCheckForm**

    from ..datacenter import DatacenterCheckForm

The BaseCheckForm class contains the `name` form field and is the lowest level of wtform classes that should be used with Monitor forms.

The DatacenterCheckForm class imports the TimerCheckForm which also imports the BaseCheckForm. If you import the DatacenterCheckForm class you will inherit the `name`, `timer`, and `datacenter` fields.

Most Monitors should inherit the DatacenterCheckForm. Only Monitors that do not run in an interval such as Webhook Monitors should inherit the BaseCheckForm directly.

#### Example Monitor form

The below example will show a Monitor form class that has two fields, one for an IP and one for a Port.

    from wtforms import Form, TextField
    from wtforms.validators import DataRequired, IPAddress, NumberRange
    from ..datacenter import DatacenterCheckForm

    class CheckForm(DatacenterCheckForm):
      ''' Class that creates a Check form for the dashboard '''
      ip = TextField("IP", validators=[IPAddress(message='Does not match IP address format')])
      port = TextField("Port", validators=[NumberRange(message='Port must be a number between 1 and 65535')])

    if __name__ == '__main__':
      pass

If we wanted to add a second field that contains a `hostname` we could add it by just adding another `TextField` object to the class.

    class CheckForm(DatacenterCheckForm):
      ''' Class that creates a Check form for the dashboard '''
      ip = TextField("IP", validators=[IPAddress(message='Does not match IP address format')])
      port = TextField("Port", validators=[NumberRange(message='Port must be a number between 1 and 65535')])
      hostname = TextField("Hostname", validators=[DataRequired(message='Hostname is a required field')])

### Step 2: The Monitor form HTML

Step #1 defines what fields should be present in the form. Step #2 actually renders the web form page. The easiest way to create a new web form page is to simply copy an existing template and modify the input fields; a good reference would be the [http-keyword](https://github.com/asm-products/cloudroutes-static/blob/master/templates/monitors/http-keyword.html) template.

#### Example form field

The below is an example form input field written in HTML and [Jinja2](http://jinja.pocoo.org/). Jinja2 is the templating language used in Flask.

    <div class="form-group">
    <label for="Host" class="col-sm-4 control-label">Domain to request</label>
      <div class="col-sm-8">
      {% if data['edit'] %}
      {{ form.host(class_="form-control", value=data['monitor']['data']['host']) }}
      {% else %}
      {{ form.host(class_="form-control", placeholder="example.com") }}
      {% endif %}
      </div>
    </div>

As you can see Jinja2 offers the ability to use if statements within the template. In the above example, if the page is in edit mode the value of `data['edit']` will be `True` and the form will be pre-filled with the value of `data['monitor']['data']['host']`. If the value of `data['edit']` is `False` the form field will be created and the placeholder value will be displayed.

This HTML is an example of how the templates above render when `data['edit']` is `False`.

    <div class="form-group">
    <label for="Host" class="col-sm-4 control-label">Domain to request</label>
    <div class="col-sm-8">
    <input class="form-control" id="host" name="host" placeholder="example.com" type="text" value="">
    </div>
    </div>

#### some-monitor.js

When the Monitor page is loaded via the main `web.py`, a `.js` file of the same name is also loaded. This file is used for the JavaScript required to activate popover help text. However, it should also be utilized for any other JavaScript-related code that needs to be imported at the footer of the Monitor page.

Even if popover text or any other JavaScript code is not utilized for this Monitor, it is required that a `.js` file is present. You can simply create a blank file if necessary.

    $ touch static/templates/monitors/some-monitor.js

#### Processing the form

As a development team, our goal is to ensure that everything is modular. When you create a new Monitor you do not need to create code to process the web form inputs. This is done automatically via the web application. It is important, however, to understand how this processing takes place.

When the web app processes the new Monitor, the details will be stored into the `monitors` table in RethinkDB, which is a JSON-based database. When you edit a Monitor the web application will query RethinkDB and store the details of that Monitor into `data['monitor']`. Below is an example of the structure of both the database and `data['monitor']`.

    data['monitor'] = {
      "ctype":  "http-keyword" ,
      "data": {
        "datacenter": [
          "dc1queue" ,
          "dc2queue"
        ] ,
        "host":  "example.com" ,
        "keyword":  "Test" ,
        "name":  "Status Check" ,
        "present":  "True" ,
        "reactions": [
          "c1c0240e-1333-1333-1333-122131112" ,
          "c107250a-1333-1333-13313-abcdefghi73"
        ] ,
        "regex":  "True" ,
        "timer":  "5mincheck" ,
        "url": "http://127.0.0.1/blah.html",
      } ,
      "failcount": 1583 ,
      "id":  "adfasdlkjfsdkljasdf98f0-1a2dbdea2675" ,
      "name":  "Example HTTP" ,
      "status":  "true" ,
      "uid":  "sdfsaasdfjlaksdfaskj369-15888dd98382" ,
      "url":  "asdfweqrue0rj2302309rur20cdsa09dafw09iacs09caswekflkwjqfklwejfjf.qwerzPHUz7heZ6VxA"
    }

When a Monitor form is submitted, the web application will process the form and define the `ctype`, `name`, `failcount`, `status`, `uid`, and `url` keys. The application will then take all of the form's inputs and put them into a dictionary under the `data` key. This system gives us the ability to create new Monitors without having to redefine or customize anything outside of the web form itself.

In simpler terms, the data key can change between Monitor types. The other fields in `data['monitor']` are meta fields that exist for every monitor.

### Step 3: Creating the actual Monitor code

Steps #1 and #2 were specifically related to creating the web elements of a Monitor. Step #3 is the creation of the actual Monitor module itself. There are two main types of Monitors in Runbook, Webhook-based Monitors and non Webhook-based Monitors.

#### Webhook-based Monitors

An example of an Webhook-based Monitor would be the [datadog-webhook](https://github.com/asm-products/cloudroutes-service/blob/master/src/web/monitorapis/datadog-webhook/__init__.py) Monitor. The end point for Webhook-based Monitors is `/api/<short-name>/<monitor id>`. The short-name in our example would be `some-monitor` and the ID would be the `id` key for the Monitor in the database. When this end point is called, the web application will try to load a python module `monitorapis/<short-name>`. If the module does not exist there is an error, if the module does exist then the web application will call the `webCheck` method from that module.

#### Example Webhook Monitor

The following is an example of a simple Webhook-based Monitor that always marks the Monitor false when called.

    def webCheck(request, monitor, urldata, rdb):
      ''' Process the webbased api call '''
      replydata = {
        'headers': { 'Content-type' : 'application/json' }
        }
      jdata = request.json

      ## Delete the Monitor
      monitor.get(urldata['cid'], rdb)
      if jdata['check_key'] == monitor.url and urldata['atype'] == monitor.ctype:
        monitor.healthcheck = "false"
        result = monitor.webCheck(rdb)
      replydata['data'] = "{'success':'True'}"
      return replydata

When the `webCheck` method is called it will be given 4 arguments; `request`, `monitor`, `urldata` and `rdb`. The `request` argument is the full `request` object from Flask. This contains all POST data and headers of the Webhook request. The `monitor` argument is an object for the `Monitor` class. In the example above we use the `get`, `healthcheck` and `webCheck` methods from this class.

The `urldata` argument is a dictionary that contains data from the URL making the request. The dictionary contains `cid`, `atype`, `check_key` and `action`. The `cid` is the Monitor ID value passed from the URL, this is not a validated ID and should be treated the same as any user input. The `atype` value is the type of Webhook being requested, this is essentially the `ctype` key in the Monitor's meta data. The `check_key` is an optional URL parameter. If it exists in the URL it can be compared with `monitor.url` as a validator, this is essentually an API Key. The `action` key is also an optional URL parameter, and is used in webhook requests to specify false or true requests.

The `rdb` object is a connection object to the RethinkDB database store.

If the POST data in the above example contains a JSON string that has a key `check_key` and that key is the same as the `monitor.url` objects value, and the `atype` value is the same as the `monitor.cytype` objects value, then the `monitor.healthcheck` object will be set to `false` and the `monitor.webCheck` method will be called. This method will send a health check message to the backend [bridge](https://github.com/asm-products/cloudroutes-service/tree/master/src/bridge) process. This process will process the false Monitor and perform necessary Reactions.

To get started with a new Webhook-based Monitor you will first need to create a new directory with the short-name under the `web/monitorapis` directory and then create an `__init__.py` file that contains the Webhook processing code.

    $ mkdir web/monitorapis/some-monitor
    $ vi web/monitorapis/some-monitor/__init__.py

#### Non Webhook-based Monitors

Non Webhook-based Monitors are Monitors that are run via [monitors](https://github.com/asm-products/cloudroutes-service/tree/master/src/monitors). These Monitors are executed from Runbook. You can think of these as external Monitors. At the moment of this writing, most of these have to do with checking a server/application externally. Using the [http-keyword](https://github.com/asm-products/cloudroutes-service/tree/master/src/cram/checks/http-keyword) Monitor as an example is the best place to start. All Monitors that run through `monitors` are Python modules placed into the `checks/` directory.

Much like using the wtforms module in step #1 to create a new Monitor, simply create a directory with the short-name and a `__init__.py` file.

    $ mkdir monitors/checks/some-monitor
    $ vi monitors/checks/some-monitor/__init__.py

The only requirement for this Monitor is to have a single method called `check()` defined. The `check()` method is a keyword arguments defined method. When `src/monitors/worker.py` calls the `check()` method, it specifies values for `jdata` and `logger`.

#### Example of `jdata`

Below is an example of what the `jdata` dictionary contains.

    data = {
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

The key item of this Monitor is the `jdata['data']` dictionary. The `jdata['data']` dictionary holds all of the form values from steps #1 and #2. For most Monitors, the details are located in this dictionary.

#### What to do after the health check is performed

The actual code to perform the health check really depends on the health check itself, but once you determine if the check was "true" the check function should return `True`. If the monitor is determined "false" the return value should be `False`.

#### Example Health Check: http-get-statuscode

The following Monitor code is from the `http-get-statuscode` Monitor and can be used as a guide on how to write a `monitors`-based Monitor.

    def check(**kwargs):
        """ Perform a http get request and validate the return code """
        jdata = kwargs['jdata']
        logger = kwargs['logger']
        headers = {'host': jdata['data']['host']}
        timeout = 3.00
        url = jdata['data']['url']
        try:
            result = requests.get(
                url, timeout=timeout, headers=headers, verify=False)
        except Exception as e:
            line = 'http-get-statuscode: Reqeust to {0} sent for monitor {1} - ' \
                   'had an exception: {2}'.format(url, jdata['cid'], e)
            logger.error(line)
            return False
        rcode = str(result.status_code)
        if rcode in jdata['data']['codes']:
            line = 'http-get-statuscode: Reqeust to {0} sent for monitor {1} - ' \
                   'Successful'.format(url, jdata['cid'])
            logger.info(line)
            return True
        else:
            line = 'http-get-statuscode: Reqeust to {0} sent for monitor {1} - ' \
                   'Failure'.format(url, jdata['cid'])
            logger.info(line)
            return False

###### Example Health Check: always-true

The following Monitor code will always return `True`, which means the Monitor itself will always be `true`.

    def check(**kwargs):
      ''' Always return true '''
      return True

#### Getting help

At this point you should at least have a Monitor that mostly works. If you're stuck and need some help, feel free to drop by our [chat](https://assembly.com/chat/runbook) page.

---
