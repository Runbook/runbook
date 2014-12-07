## Webhook

Users of PaperTrail can define unique [Alerts](http://help.papertrailapp.com/kb/how-it-works/alerts/) that call outside services such as Email, PagerDuty or even a generic Webhook. This monitor will create a unique webhook endpoint that you can configure PaperTrail to call when it detects an Alert. This integration allows you to combine Runbook Reactions with PaperTrail alerts.

### URL Details

Upon creating the monitor you will be provided with two unique URL's. These URL's can be the destination of the PaperTrail webhook.

**Unique False URL:**

    https://dash.runbook.io/api/papertrail-webhook/example-api-id/example-api-key/false

**Unique True URL:**

    https://dash.runbook.io/api/papertrail-webhook/example-api-id/example-api-key/true

Since PaperTrail does not send true webhook events this monitor has two URLs, one for false alerts and another for true alerts. Once a monitor is marked false it will not be marked true until the true URL is also called. It is best practice for every false alert in PaperTrail to create a second alert for true states.

#### URL Secrecy

It is important to note that PaperTrail does not provide a way to authenticate the request. With that in mind authentication is performed by simply requesting the above URL's. These are unique per monitor but should be treated as sensitive information.

