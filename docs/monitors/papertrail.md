## Webhook

Users of [PaperTrail](http://www.papertrailapp.com) can define unique [Alerts](http://help.papertrailapp.com/kb/how-it-works/alerts/) that call outside services such as email, PagerDuty, or even a generic webhook. This Monitor will create a unique webhook endpoint that you can configure PaperTrail to call when it detects an Alert. This integration allows you to combine Runbook Reactions with PaperTrail alerts.

### URL details

Upon creating the Monitor, you will be provided with two unique URLs. These URLs can be the destination of the PaperTrail webhook.

**Unique False URL:**

    https://dash.runbook.io/api/papertrail-webhook/example-api-id/example-api-key/false

**Unique True URL:**

    https://dash.runbook.io/api/papertrail-webhook/example-api-id/example-api-key/true

Since PaperTrail does not send true webhook events, this Monitor has two URLs, one for false alerts and another for true alerts. Once a Monitor is marked false it will not be marked true until the true URL is also called. It is best practice for every false alert in PaperTrail to create a second alert for true states.

#### URL Secrecy

It is important to note that PaperTrail does not provide a way to authenticate the request. With that in mind, authentication is performed by simply requesting the above URLs. These URLs are unique for each Monitor but should be treated as sensitive information.

---