## Webhook

Users of [Logentries](https://logentries.com) can define unique [Alerts](https://logentries.com/doc/tagsalerts/) that call outside services such as email, PagerDuty, or even a generic webhook. This Monitor will create a unique webhook endpoint that you can configure Logentries to call when it detects an Alert. This integration allows you to combine Runbook Reactions with Logentries alerts.

---

### URL Details

Upon creating the Monitor, you will be provided with two unique URLs. These URLs can be the destination of the Logentries webhook.

**Unique False URL:**

    https://dash.runbook.io/api/logentries-webhook/example-api-id/example-api-key/false

**Unique True URL:**

    https://dash.runbook.io/api/logentries-webhook/example-api-id/example-api-key/true

Since Logentries does not send true webhook events, this Monitor has two URLs, one for false alerts and another for true alerts. Once a Monitor is marked false it will not be marked true until the true URL is also called. It is best practice for every false alert in Logentries to create a second alert for true states.

#### URL Secrecy

It is important to note that Logentries does not provide a way to authenticate the request. With that in mind, authentication is performed by simply requesting the above URLs. These URLs are unique for each Monitor but should be treated as sensitive information.

---