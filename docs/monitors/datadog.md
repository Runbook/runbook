## Webhook

The **Datadog: Webhook** Monitor is a webhook-based Monitor. This type of Monitor does not run at a regular interval, but rather listens on a unique URL for webhook requests. Within Datadog you can setup an [integration for webhook requests](http://docs.datadoghq.com/integrations/webhooks/). When defining metric alerts within Datadog you can simply tag the webhook integrations. When an alert is triggered, Datadog will then send a webhook to the unique URL provided.

This Monitor allows users to integrate Runbook Reactions with existing monitoring systems. It also allows users to monitor local system status that Runbook would not be able to see externally.

## URL and Key

After creating a **Datadog: Webhook Monitor** you will be given a unique `url` and `check_key`. The `url` value is the target for Datadog's webhooks and is unique for each Monitor.

    url: https://dash.runbook.io/api/datadog-webhook/example-api-id
    check_key: example-api-key

## Custom Payload

When using Datadog's webhook integration you will need to specify a custom payload. This payload must include the `check_key` and `title` attributes at minimum. Additional details can be included, but they are not used for processing the Monitor data.

    { 
        "check_key": "example-api-key",
        "title" : "$EVENT_TITLE"
    }

---