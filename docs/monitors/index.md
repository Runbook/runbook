Monitors are triggers used to check the status of your environment. A Monitor can include many types of triggers. They may perform an HTTP GET request or simply listen for webhooks from GitHub.

In general, Runbook consists of two types of Monitors:

1. Monitors that run at a scheduled interval
2. Monitors that listen for webhooks

[Reactions](../reactions/index.md) are automated tasks that are called when Monitors fail. When creating a Reaction, it is important to know what type of Monitor it is being attached to. In general, webhook Monitors will receive triggering events less often than Monitors that run at scheduled intervals.

* [Network Availability](network-availability.md)
* [Web Applications](web-applications.md)
* [Heroku](heroku.md)
* [Datadog](datadog.md)
* [Papertrail](papertrail.md)
* [Logentries](logentries.md)
* [Runbook Webhooks](runbook-webhooks.md)

Can't find a Monitor you want? [Make a suggestion](https://assembly.com/runbook/bounties/80) on our Assembly project page.

---
