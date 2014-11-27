# Creating Monitors

This installation guide will help you with your initial setup of [Runbook](https://runbook.io).


## Introduction

With Runbook, we have kept the creation of monitors as simple as possible by making the Monitors modular. Creating a new Monitor doesn't require you to edit the main `web.py` file, but rather requires you to create several new files that are dynamically loaded into the application.

When creating a new Monitor, it is important to define a **short-name** for the Monitor. This short-name will be used throughout the various modules you create to uniquely identify the Monitor.

**For example:** An HTTP GET-based Monitor that searches for a specific keyword, has a short-name of `http-keyword`. This short-name is unique for this type of Monitor and all files created for this Monitor reference the short-name.

In this guide we will be using the `http-keyword` Monitor as reference. This Monitor is a Non-API based Monitor and is a good example of how simple a Monitor is to create.


## Creating a new Monitor


### Step 1: The Monitor web form

Runbook is written using the [flask](http://flask.pocoo.org/) framework. A common utility for creating web forms within flask is [wtforms](https://wtforms.readthedocs.org/en/latest/). We utilize wtforms for all web forms within the Runbook GUI, including the forms that create Monitors.

For this document, we will create a new Monitor named `some-monitor`; the first step of creating a Monitor is to create the web form needed for users. To start the web form we will create a directory in `crweb/monitorforms/` called `some-monitor`. Within that directory we will create a `__init__.py` file containing a class that defines the required form fields. 

    $ mkdir crweb/monitorforms/some-monitor
    $ vi crweb/monitorforms/some-monitor/__init__.py

Within this file is the actual wtforms code. You can use the [http-keyword](https://github.com/asm-products/cloudroutes-service/blob/master/src/crweb/monitorforms/http-keyword/__init__.py) Monitor as an example.

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

Most Monitors should inherit the DatacenterCheckForm. Only Monitors that do not run in an interval such as API Monitors should inherit the BaseCheckForm directly.


#### Example Monitor form

The below example will show an example Monitor form class that has two fields, one for an IP and one for a Port.

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

The below is an example form input field written in HTML and [Jinja2](http://jinja.pocoo.org/); Jinja2 is the templating language used in Flask.

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

As you can see Jinja2 offers the ability to use if statements within the template. In the above example if we are in edit mode `data['edit']` will be `True` and the form will be pre-filled with the value of `data['monitor']['data']['host']`. If the value of `data['edit']` is `False` the form field will be created and the placeholder value will be displayed.

The below HTML is an example of the above templates rendering when `data['edit']` is `False`.

    <div class="form-group">
    <label for="Host" class="col-sm-4 control-label">Domain to request</label>
    <div class="col-sm-8">
    <input class="form-control" id="host" name="host" placeholder="example.com" type="text" value="">
    </div>
    </div>

#### some-monitor.js

When the Monitor page is loaded via the main `web.py`, a `.js` file of the same name is also loaded. This file is used for the JavaScript required to activate popover help text, however it should also be utilized for any other JavaScript-related code that needs to be imported at the footer of the Monitor page.

Even if popover text or any other JavaScript code is not utilized for this Monitor it is required that a `.js` file is present. You can create a blank file if necessary.

    $ touch static/templates/monitors/some-monitor.js

#### Processing the form

As a development team, our goal is to ensure that everything is modular. When you create a new Monitor you do not need to create code to process the web form inputs. This is done automatically via the web application. It is important, however, to understand how this processing takes place.

When the web app processes the new Monitor the details will be stored into the monitors table in RethinkDB, which is a JSON-based database. When you edit a Monitor the web application will query RethinkDB and store the details of that Monitor into `data['monitor']`. Below is an example of the structure of both the database and `data['monitor']`.

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
      "status":  "healthy" ,
      "uid":  "sdfsaasdfjlaksdfaskj369-15888dd98382" ,
      "url":  "asdfweqrue0rj2302309rur20cdsa09dafw09iacs09caswekflkwjqfklwejfjf.qwerzPHUz7heZ6VxA"
    }

When a Monitor form is submitted, the web application will process the form and define the `ctype`, `name`, `failcount`, `status`, `uid`, and `url` keys. The application will then take all of the form's inputs and put them into a dictionary under the `data` key. This system gives us the ability to create new Monitors without having to redefine or customize anything outside of the web form itself.

In simpler terms, the data key can change between Monitor types. The other fields in `data['monitor']` are meta fields that exist for every monitor.


### Step 3: Creating the actual Monitor code

Step #1 and #2 were all about creating the web elements of a Monitor. Step #3 is actually creating the Monitor module itself. There are two main types of Monitors in Runbook, API-based Monitors and non API-based Monitors.

#### API-based Monitors

An example of an API-based Monitor would be the [datadog-webhook](https://github.com/asm-products/cloudroutes-service/blob/master/src/crweb/monitorapis/datadog-webhook/__init__.py) monitor. The end point for API-based Monitors is `/api/<short-name>/<monitor id>`. The short-name in our example would be `some-monitor` and the ID would be the `id` key for the Monitor in the database. When this end point is called, the web application will try to load a python module `monitorapis/<short-name>`. If the module does not exist there is an error, if the module does exist then the web application will call the `webCheck` method from that module.

#### Example API Monitor

The following is an example of a simple API-based Monitor that always marks the Monitor failed when called.

    def webCheck(request, monitor, urldata, rdb):
      ''' Process the webbased api call '''
      replydata = { 
        'headers': { 'Content-type' : 'application/json' }
        }
      jdata = request.json
       
      ## Delete the Monitor
      monitor.get(urldata['cid'], rdb)
      if jdata['check_key'] == monitor.url and urldata['atype'] == monitor.ctype:
        monitor.healthcheck = "failed"
        result = monitor.webCheck(rdb)
      replydata['data'] = "{'success':'True'}"
      return replydata

When the `webCheck` method is called it will be given 4 arguments; `request`, `monitor`, `urldata` and `rdb`. The `request` argument is the full `request` object from Flask, this contains all POST data and Headers of the API request. The `monitor` argument is an object for the `Monitor` class, in the example above we use the `get`, `healthcheck` and `webCheck` methods from this class.

The `urldata` argument is a dictionary that contains data from the URL making the request. The dictionary contains `cid`, `atype`, `check_key` and `action`. The `cid` is the Monitor ID value passed from the URL, this is not a validated ID and should be treated the same as any user input. The `atype` value is the type of API being requested, this is essentially the `ctype` key in the monitors meta data. The `check_key` is an optional URL parameter, if it exists in the URL it can be compared with `monitor.url` as a validator, this is essentually an API Key. The `action` key is also an optional URL parameter, and is used in webhook requests to specify failed or healthy requests.

The `rdb` object is a connection object to the RethinkDB database store.

In the above example if the POST data contains a JSON string that has a key `check_key` and that key is the same as the `monitor.url` objects value, and the `atype` value is the same as the `monitor.cytype` objects value. The `monitor.healthcheck` object will be set to `failed` and the `monitor.webCheck` method will be called. This method will send a health check message to the backend [crbridge](https://github.com/asm-products/cloudroutes-service/tree/master/src/crbridge) process. This process will process the failed monitor and perform necessary reactions.

To get started with a new API-based Monitor you will first need to create a new directory with the short-name under the `crweb/monitorapis` directory and then create an `__init__.py` file that contains the API processing code.

    $ mkdir crweb/monitorapis/some-monitor
    $ vi crweb/monitorapis/some-monitor/__init__.py

#### Non API-based Monitors

Non API-based Monitors are Monitors that are run via [cram](https://github.com/asm-products/cloudroutes-service/tree/master/src/cram). These monitors are executed from Runbook. You can think of these as external Monitors. At the moment of this writing, most of these have to do with checking a server/application externally. Using the [http-keyword](https://github.com/asm-products/cloudroutes-service/tree/master/src/cram/checks/http-keyword) Monitor as an example is the best place to start. All Monitors that run through `cram` are python modules placed into the `checks/` directory. 

Much like using the wtforms module in Step #1 to create a new Monitor, simply create a directory with the short-name and a `__init__.py` file.

    $ mkdir cram/checks/some-monitor
    $ vi cram/checks/some-monitor/__init__.py

The only requirement for this Monitor is to have a single method called `check`. This method will be given `data` which is a dictionary that contains the Monitor information from the database as well as some extra information from the `cram/control.py` process.

#### Example of `data`

Below is an example of what the `data` dictionary contains.

    data = {
      "status": "failed",
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

The key item of this Monitor is the `data['data']` dictionary. The `data['data']` dictionary holds all of the form values from Step #1 and #2. For most Monitors the details are located in this dictionary.


#### What to do after the health check is performed

The actual code to perform the health check really depends on the health check itself, but once you determine if the check was "healthy" the check function should return `True`. If the monitor is determined "failed" the return value should be `False`.


#### Example Health Check: http-get-statuscode

The following monitor code is from the `http-get-statuscode` Monitor and can be used as a guide on how to write a `cram` based Monitor.

    def check(data):
      """ Perform a http get request and validate the return code """
      headers = { 'host' : data['data']['host'] }
      timeout = 3.00
      url = data['data']['url']
      try:
        result = requests.get(url, timeout=timeout, headers=headers, verify=False)
      except:
        return False
      rcode = str(result.status_code)
      if rcode in data['data']['codes']:
        return True
      else:
        return False


###### Example Health Check: always-true

The following Monitor code will always return `True`, which means the Monitor itself will always be `healthy`.

    def check(data):
      ''' Always return healthy '''
      return True


#### Getting help

At this point you should have at least a Monitor that mostly works. If you're stuck and need some help, feel free to drop by our [chat](https://assembly.com/chat/runbook) page.


---

# Creating Reactions


## Introduction

With Runbook, we have kept the creation of Reactions as simple as possible by making the Reactions modular. Creating a new Reaction doesn't mean that you have to edit the main `web.py` file, but rather requires you to create several new files that are dynamically loaded into the application.

When creating a new Reaction it is important to define a **short-name** for the Reaction. This short-name will be used throughout the various modules you create to uniquely identify the Reaction.

**For Example:** We have recently deployed a Reaction for Restarting AWS EC2 instances into production, the short-name for this reaction is `aws-ec2restart`. This short-name is unique for this type of Reaction and all files created for Rhis reaction reference this short-name.

In this guide we will use the `aws-ec2restart` Reaction as an example.

## Creating a new Reaction

### Step 1: The Reaction web form

Runbook is written using the [flask](http://flask.pocoo.org/) framework. A common utility for creating web forms within flask is [wtforms](https://wtforms.readthedocs.org/en/latest/). We utilize wtforms for all web forms within the Runbook GUI, including the forms that create Reactions.

For this document, we will create a new Reaction named `some-reaction`. The first step of creating a Reaction is to create the web form needed for users. To start the web form we will create a directory in `crweb/reactions` called `some-reaction`. Within that directory we will create a `__init__.py` file that will contain a class that defines the form fields required.

    $ mkdir crweb/reactionforms/some-reaction
    $ vi crweb/reactionforms/some-reaction/__init__.py

Within this file is the actual wtforms code. You can use the [aws-ec2restart](https://github.com/asm-products/cloudroutes-service/blob/master/crweb/reactionforms/aws-ec2restart/__init__.py) Reaction as an example.

There are a couple of guidelines when creating a web form for Reactions.

* The class must be named ReactForm

When the main web component loads the form it will dynamically load the ReactForm class. This dynamic loading relies on the short-name and is pulled from the URL the user navigates to.

* The class should inherit BaseReactForm

The BaseReactForm contains base fields that every Reaction should contain. You should inherit this class to ensure you have at least the base Reaction requirements. You can import this class with the following.

    from ..base import BaseReactForm

###### Example Reaction form

The simplest example can be seen below.

    from wtforms import Form, TextField
    from wtforms.validators import DataRequired
    from ..base import BaseReactForm
    
    class ReactForm(BaseReactForm):
      ''' Class that creates a Reaction form for the dashboard '''
      example_field = TextField("Example Field", validators=[DataRequired(message="Example Field is a required field")])
      
    if __name__ == '__main__':
      pass

The above will create a form object that has all of the base required fields and a new field named `example_field`. To add more fields simply add them to the class. 

As an example the below class would create a form that had all of the base fields and two additional fields, one for an API key and another for a Resource ID.

    class ReactForm(BaseReactForm):
        ''' Class that creates a Reaction form for the dashboard '''
        api_key = TextField("API Key", validators=[DataRequired(message="API Key is a required field")])
        resource_id = TextField("Resource ID", validators[DataRequired(message="Resource ID is a required field")])


### Step 2: Reaction form HTML

Where Step #1 created the web form object for Flask, Step #2 is about creating the HTML & [Jinja2](http://jinja.pocoo.org/) template files that render the web form. The easiest way to create a new template is to simply copy an existing one. A good example template is the [aws-ec2restart.html](https://github.com/asm-products/cloudroutes-service/blob/master/static/templates/reactions/aws-ec2restart.html) Reaction.

The majority of the `aws-ec2restart.html` file is a basic page structure; for the most part the structure of each Reaction page does not change from Reaction to Reaction. The main components that change are the form fields themselves.

#### Example form field

Below is an example of an input field written in HTML and Jinja2.

    <div class="form-group">
      <label for="AWS Access Key" class="col-sm-4 control-label">AWS Access Key</label>
      <div class="col-sm-8">
        <div class="input-group">
          <span class="input-group-btn">
            <button type="button" id="aws-access-key" class="btn btn-default" rel="popover" data-content="This field should contain your AWS Access Key, which can be obtained from the AWS Management Console." title="AWS Access Key"><i class="fa fa-question"></i></button>
          </span>
          {% if data['edit'] %}
            {{ form.aws_access_key(class_="form-control", value=data['reaction']['data']['aws_access_key']) }}
          {% else %}
            {{ form.aws_access_key(class_="form-control", placeholder="AWS Access Key") }}
          {% endif %}
        </div>
      </div>
    </div>

As you can see Jinja2 accepts if statements. In this example, if the page is in edit mode `data['edit']` will be `True`. As per the template if `data['edit'` is `True`, the web form field `aws_access_key` will be created and pre-populated with the value of `data['reaction']['data']['aws_access_key']`. If the value of `data['edit']` is `False` the form field will be created and the placeholder value will be displayed.

When the page is rendered the above template code will turn into the below HTML.

    <div class="form-group">
    <label for="AWS Access Key" class="col-sm-4 control-label">AWS Access Key</label>
    <div class="col-sm-8">
    <div class="input-group">
    <span class="input-group-btn">
    <button type="button" id="aws-access-key" class="btn btn-default" rel="popover" data-content="This field should contain your AWS Access Key, which can be obtained from the AWS Management Console." title="AWS Access Key"><i class="fa fa-question"></i></button>
    </span>
    <input class="form-control" id="aws_access_key" name="aws_access_key" placeholder="AWS Access Key" type="text" value="">
    </div>
    </div>
    </div>

##### Classes for form fields

If you look at the Jinja2 code in the template you will notice the `class_="form-control"` was translated to `class="form-control"` in the HTML. The Runbook GUI has several form classes that should be used depending on the form type. Below is the list and what they are used for.

* form-control - General purpose bootstrap form field class
* select - Used for `SelectField` form fields and is provided by `bootstrap-multiselect.css`
* multiselect - Used for `MultiSelectField` form fields and is provided by `bootstrap-multiselect.css`

It is important to utilize the appropriate class to ensure a consistent visual appearance on the Runbook dashboard.

#### some-reaction.js

When the Reaction page is loaded via the main `web.py`, a `.js` file of the same name is also loaded. This file is used for the JavaScript required to activate popover help text. However, it should also be utilized for any other JavaScript related code that needs to be imported at the footer of the page. Even if popover text or any other JavaScript code is not utilized for this Reaction it is required that a `.js` file is present. You can simply create a blank file if necessary.

    $ touch static/templates/reactions/some-reaction.js

#### Processing the form

As a development team, our goal is to ensure that everything is modular. When you create a new Reaction you do not need to create code to process the web form inputs. This is done automatically via the web application. It is important however to understand how this processing takes place. 

When the web app processes the new Reaction the details will be stored into the `reactions` table in RethinkDB, which is a JSON-based database. When you edit a Reaction the web application will query RethinkDB and store details about that Reaction into `data['reaction']`. Below is an example of the structure of both the database and `data['reaction']`.

    data['reaction'] = {
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

The above example is a Reaction entry from a `cloudflare-ip-remove` Reaction. When the web application processes the creation form it will place the `name`, `frequency`, and `trigger` fields under the `data['reaction']` dictionary. All other fields are placed into the `data['reaction']['data']` dictionary. This is a similar format to what the actual Reaction code will see as well.

### Step 3: Creating the actual Reaction code

Steps #1 and #2 were specifically related to creating the web elements of a Reaction. Step #3 is the creation of the Reaction module itself. 

#### Creating a new Reaction

Reactions are essentially python modules that are called by another process. To create a new Reaction you will first need to create a directory using the short-name in the `crbridge/actions` directory, then create a `__init__.py` file that contains the Reaction code.

    $ mkdir crbridge/actions/some-reaction
    $ vi crbridge/actions/some-reaction/__init__.py

A good reference file would be the [aws-ec2restart](https://github.com/asm-products/cloudroutes-service/blob/master/crbridge/actions/aws-ec2restart/__init__.py) Reaction.

#### How Reactions are called

In each datacenter/monitoring zone there is a process running that is sometimes referred to as **"the sink"**, this process is executing [crbridge/actioner.py](https://github.com/asm-products/cloudroutes-service/blob/master/crbridge/actioner.py). This process will bind a port and listen for [ZeroMQ](http://zeromq.org/) messages. These messages are the results of health checks from both the web application and [cram/worker.py](https://github.com/asm-products/cloudroutes-service/blob/master/cram/worker.py). 

When the `actioner.py` receives a ZeroMQ message it converts the JSON message into a dictionary. The `actioner.py` will then look up details from Redis and RethinkDB for both the Monitor and all associated Reactions. For each Reaction defined in the Monitor it will load the Reaction module `actions/<short-name>` and execute either the `failed` or `healthy` methods.

When a Monitor is healthy, `actioner.py` will call the Reaction's `healthy` method. When a Monitor is failed, `actioner.py` will call the `failed` method.

The `actioner.py` process calls these methods with 4 objects: `redata`, `jdata`, `rdb_server` and `r_server`. The `redata` object contains a dictionary of the specific Reaction pulled from the database/cache. The `jdata` object contains a dictionary of the JSON message received with some additional fields required for executing Reactions. The `rdb_server` is an object required for the connection to the RethinkDB instance. The `r_server` is an object required for the connection to the Redis instance.

Below are examples of the `redata` and `jdata` dictionaries.

##### redata

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

As you can see this is exactly what was queried from the database store.

##### jdata

    jdata = {
      "status": "failed",
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
        "status": "healthy",
        "prev_status": "healthy",
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

Depending on the type of monitor the `data` key may contain different keys and values but all other fields from the above example will exist.

#### Processing reactions

Once `actioner.py` invokes the `failed` or `healthy` method from a Reaction, it is up to the Reaction itself to determine what it should do. The decision on whether the Reaction should actually be executed or not depends on the configuration of each action and is placed solely on the Reaction's code. While this does vary from Reaction to Reaction, there are a couple of set rules for processing Reactions.

1) The Reaction must honor trigger and frequency settings

In Runbook, we have implemented a feature called `trigger` and `frequency`. These two settings allow users to define the number of `healthy` or `failed` checks that must be returned before Reaction execution and the frequency between Reaction executions.

The trigger value is stored in `redata['trigger']` and this can be compared with `jdata['failcount']`. The frequency value is the number of seconds between executions, is stored in `redata['frequency']`, and can be compared with `jdata['lastrun']` which is a timestamp of when the Reaction was last executed.

Some Reactions may require additional processing rules. Each Reaction is free to define additional fields in the web form that only have the purpose of determining whether the Reaction should be executed. An example of this is the `jdata['data']['call_on']` field in the `aws-ec2restart` Reaction. This field allows users to define if the restart should happen on `healthy` or `failed` monitors.

The below example is an excerpt of the [aws-ec2restart](https://github.com/asm-products/cloudroutes-service/blob/master/crbridge/actions/aws-ec2restart/__init__.py) Reaction.

    def failed(redata, jdata, rdb, r_server):
      ''' This method will be called when a monitor has failed '''
      run = True
      ## Check for Trigger
      if redata['trigger'] > jdata['failcount']:
        run = False
    
      ## Check for lastrun
      checktime = time.time() - float(redata['lastrun'])
      if checktime < redata['frequency']:
        run = False
    
      if redata['data']['call_on'] == 'healthy':
        run = False
    
      if run:
        return actionEC2(redata, jdata)
      else:
        return None

The above is a simple example of how to perform the above processing rules.

2) The return code is important

After a reaction has executed, it is important that an appropriate return code is used. The `actioner.py` process is expecting either a `True`, `False` or `None` return; depending on which value is returned will determine the state of the Reaction's execution. Below is a list of return value and what that value means to `actioner.py`.

* `True` - Reaction was processed successfully
* `False` - Reaction attempted to process but failed
* `None` - Reaction processing was skipped

If we review the sample code above, we can see that the return value is set to `None` if the Reaction's function `actionEC2` was not executed. This tells the `actioner.py` process that the Reaction was not executed.

      if run:
        return actionEC2(redata, jdata)
      else:
        return None

The return value to the `actioner.py` is important as it is used to determine whether the `lastrun` value of the reaction should be updated. It is also used for historical tracking of Monitors and Reactions, and tells users when Reactions were executed or not.

## Getting help

Runbook is developed as part of Assembly. If you have any questions while developing a new monitor, feel free to drop by our [chat](https://assembly.com/chat/runbook) page.

---