Reactions are automated tasks that are called when Monitors fail. At the moment Runbook reactions are made by integrating with outside services such as Heroku, CloudFlare and Commando. You can utilize these reactions to perform everything from restarting Apache via Commando to Rolling back to a previous application version with Heroku.

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

Reaction creation can be a bit complicated, this section hopes to explain some of the more complicated concepts.

### Trigger

The `Trigger` field is used to denote how many times a monitor must return the desired value before the reaction should be executed. This setting is useful for reactions that perform significant steps such as restarting a serivce or rebooting a server. If a monitor executes every 2 minutes and it's associated reaction has a `trigger` value of 2, the reaction would not be executed until the 2nd instance of the desired state. 

### Frequency

The `Frequency` field is used to denote how often (in seconds) a reaction should run. This setting allows you to build in time between reaction executions. If a monitor is set to execute every 2 minutes, once the monitor surpasses the `trigger` value reactions with a `frequency` of `0` will be executed each time the monitor is executed. Reactions with a `frequency` value of `360` will be executed no sooner than 6 minutes after the last reaction execution.

### Call On

The `Call On` field is used to specify whether a reaction should be executed on Healthy or Failed monitors. Not all reactions have this setting as some reactions only apply to Failed or only apply to Healthy monitors.

