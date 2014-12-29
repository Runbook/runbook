Reactions are automated tasks that are called when Monitors fail. At the moment, Runbook Reactions are made by integrating with outside services such as Heroku, CloudFlare, and Commando. You can utilize these Reactions to perform everything from restarting Apache via Commando to Rolling back to a previous application version with Heroku.

Runbook currently features Reactions for these services:

* [CloudFlare](cloudflare.md)
* [Heroku](heroku.md)
* [Commando](commando.md)
* [DigitalOcean](digitalocean.md)
* [Amazon Web Services](aws.md)
* [Rackspace](rackspace.md)
* [Saltstack](saltstack.md)
* [Notifications](notifications.md)
* [Statistics](statistics.md)

## Reaction Form Fields

Reaction creation can be a bit complicated. This section hopes to explain some of the more complicated concepts.

### Trigger

The `Trigger` field is used to denote how many times a Monitor must return the desired value before the Reaction should be executed. This setting is useful for Reactions that perform significant steps such as restarting a serivce or rebooting a server. If a Monitor executes every 2 minutes and it's associated Reaction has a `trigger` value of 2, the Reaction would not be executed until the 2nd instance of the desired state. 

### Frequency

Most Monitors are checked in a reoccuring interval, after each Monitor execution the ACTIONS processes will process the results and determine which Reactions to run. By default every Reaction will be executed once with each Monitor result until the conditions for the Reaction are no longer true. 

The `Frequency` field is used to denote how often (in seconds) a Reaction should run. This setting allows you to build a delay between Reaction executions to allow a previous Reaction execution to take effect.

If a Monitor is set to execute every 2 minutes, once the Monitor surpasses the `trigger` value Reactions with a `frequency` of `0` will be executed each time the Monitor is executed. Reactions with a `frequency` value of `360` will be executed no sooner than 6 minutes after the last Reaction execution.

### Call On

The `Call On` field is used to specify whether a Reaction should be executed on True or False Monitors. Not all Reactions have this setting as some Reactions only apply to False or True Monitors.

---
