Monitors are the triggers used to check the status of your environment. A monitor can be many types of triggers they may perform an HTTP GET request or simply listen for webhooks from GitHub.

In general Runbook consists of two types of monitors:

1. Monitors that run at a scheduled interval
2. Monitors that listen for webhooks

When creating reactions it is important to know what type of monitor it is being attached to, in general webhook monitors will receive triggering events less often than monitors that run at scheduled intervals.

* [Network Availability](network-availability.md)
* [Web Applications](web-applications.md)
* [Heroku](heroku.md)
* [Datadog](datadog.md)
* [Papertrail](papertrail.md)
* [Logentries](logentries.md)
* [Runbook Webhooks](runbook-webhooks.md)

Can't find a monitor you want? [Make a suggestion](https://assembly.com/runbook/bounties/80)
