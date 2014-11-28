# Runbook Webhooks

## Runbook: Webhooks

This monitor is a generic webhook that is specific to Runbook. When created this monitor will provide the user with a unique URL and token that allows the user to signify if the monitor is healthy or failed. While most webhook listeners do not provide information back this webhook listener is different. It is also possible to query the current state of the monitor from this webhook URL.

This webhook URL could be used to integrate tools and systems we do not already have an inherent integration with; allowing users to add Runbook reactions to many monitoring services.

### URL and Key

Upon creation the monitor form will provide a user with a unique URL and Key. 

url: https://dash.runbook.io/api/cr-api/example-webhook-id
check_key: example-webhook-token

### Requesting with JSON

The standard method of making webhook requests to the Runbook: Webhooks monitor is to send JSON data via a `POST` request to the unique URL. The JSON data requires two keys `check_key` which contains the unique token and the `action` key which defines what the request is for. Valid actions are `healthy`, `failed`, or `status`.

When sending webhook requests with JSON data it is important to set the `content-type` header to `application/json`. In addition to returning a JSON reply the webhook reply will return a status code of 200 for valid and accepted webhooks.

#### Examples

The below are examples of valid JSON webhook requests.

##### Sending a Healthy Notification

**Request**

    {
      "check_key" : "example-webhook-token",
      "action" : "healthy"
    }

**Reply**

    {
      "result": "success",
    }

##### Sending a Failed Notification

**Request**

    {
      "check_key" : "example-webhook-token",
      "action" : "failed"
    }

**Reply**

    {
      "result": "success"
    }


##### Requesting Status

**Request**

    {
      "check_key" : "example-webhook-token",
      "action" : "status"
    }
            
**Reply**

    {
      "result": "success",
      "failcount": 300,
      "status": "healthy"
    }

The JSON reply for status requests includes two new keys `status` which describes the current status of the monitor and `failcount` which is a value of the number of times this monitor has returned the current status.

##### Making a JSON based request with cURL

The below is an example of making a JSON based webhook request with cURL

    $ curl -X POST -H "Content-type: application/json" -d '{
    "check_key" : "example-webhook-token",
    "action" : "status"
    }' -k https://dash.runbook.io/api/cr-api/example-webhook-id
            
#### Requesting with the URL

Some external systems do not allow you to specify the data being sent with the webhook request. For these types of systems you can simply append the `check_key` and `action` to the URL being requests.

An example URL would look like the following.

    https://dash.runbook.io/api/cr-api/example-webhook-id/<check_key>/<action>

##### Example URL reqeusts with cURL

##### Healthy Notification

    $ curl -X POST https://dash.runbook.io/api/cr-api/example-webhook-id/example-webhook-token/healthy

##### Failed Notification

    $ curl -X POST https://dash.runbook.io/api/cr-api/example-webhook-id/example-webhook-token/failed

##### Requesting Status

    $ curl -X POST https://dash.runbook.io/api/cr-api/example-webhook-id/example-webhook-token/status
