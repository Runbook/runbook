## Webhook

This Monitor is a generic webhook that is specific to [Runbook](https://www.runbook.io). When created, this Monitor will provide the user with a unique URL and token that allows the user to signify if the Monitor is true or false. While most webhook listeners do not provide information back, this webhook listener is different. It is also possible to query the current state of the Monitor from this webhook URL.

This webhook URL could be used to integrate tools and systems we do not already have an inherent integration with; allowing users to add Runbook Reactions to many monitoring services.

## Every Monitor has a webhook endpoint

Every Monitor created on Runbook receives a unique URL and check_key token. The details of each Monitor's unique data is below the creation form. With these details all Monitors can be used with the webhook interface.

### URL and Key

Upon creation, the Monitor form will provide a user with a unique URL and Key. 

    url: https://dash.runbook.io/api/cr-api/example-webhook-id
    check_key: example-webhook-token

### Requesting with JSON

The standard method of making webhook requests to the Runbook: Webhooks Monitor is to send JSON data via a `POST` request to the unique URL. The JSON data requires two keys: `check_key` which contains the unique token, and the `action` key which defines what the request is for. Valid actions are `true`, `false`, or `status`.

When sending webhook requests with JSON data it is important to set the `content-type` header to `application/json`. In addition to returning a JSON reply, the webhook reply will return a status code of 200 for valid and accepted webhooks.

#### Examples

The below are examples of valid JSON webhook requests.

##### Sending a True notification

**Request**

    {
      "check_key" : "example-webhook-token",
      "action" : "true"
    }

**Reply**

    {
      "result": "success",
    }

##### Sending a False notification

**Request**

    {
      "check_key" : "example-webhook-token",
      "action" : "false"
    }

**Reply**

    {
      "result": "success"
    }


##### Requesting status

**Request**

    {
      "check_key" : "example-webhook-token",
      "action" : "status"
    }
            
**Reply**

    {
      "result": "success",
      "failcount": 300,
      "status": "true"
    }

The JSON reply for status requests includes two new keys: `status` which describes the current status of the Monitor, and `failcount` which is a value of the number of times this Monitor has returned the current status.

##### Making a JSON-based request with cURL

The below is an example of making a JSON-based webhook request with cURL.

    $ curl -X POST -H "Content-type: application/json" -d '{
    "check_key" : "example-webhook-token",
    "action" : "status"
    }' -k https://dash.runbook.io/api/cr-api/example-webhook-id
            
#### Requesting with the URL

Some external systems do not allow you to specify the data being sent with the webhook request. For these types of systems, you can simply append the `check_key` and `action` to the URL being requested.

An example URL would look like the following.

    https://dash.runbook.io/api/cr-api/example-webhook-id/<check_key>/<action>

##### Example URL requests with cURL

##### True notification

    $ curl -X POST https://dash.runbook.io/api/cr-api/example-webhook-id/example-webhook-token/true

##### False notification

    $ curl -X POST https://dash.runbook.io/api/cr-api/example-webhook-id/example-webhook-token/false

##### Requesting status

    $ curl -X POST https://dash.runbook.io/api/cr-api/example-webhook-id/example-webhook-token/status

## Unofficial extensions

### RunbookWraps

[RunbookWraps](https://github.com/madflojo/RunbookWraps) is a set of Python scripts that utilize Runbook's webhook interface to perform on server Monitors and Reactions. These scripts include a monitoring script that will execute defined shell commands and will notify Runbook of success or failure. The second script included is a Reaction script that requests Monitor status from Runbook webhooks and performs shell commands defined in a configuration file.

### runbook-webhook

[Runbook-webhook](https://github.com/madflojo/runbook-webhook) is a simple shell script that can be used to perform the 3 webhook requests. URL and check_key are provided via command line arguments.

---