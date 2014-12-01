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

The `Trigger` field is used to denote how many times a reaction must be identified as Healthy or Failed before execution. For example if a reaction had a trigger of 2 and the attached monitor ran every 4 minutes, the reaction would not execute until the 2nd run; 8 minutes from the first failure.

### Frequency

The `Frequency` field is used to determine how often (in seconds) a reaction should run. If a reaction is executed the execution time is stored in cache and within the database. If a subsequent monitor attempts to trigger the reaction, the reaction will not execute if the time since last execution is within the `Frequency` value. Using the same example as above if a reaction had a trigger of 2 and a frequency of 300 the reaction would not be executed until 8 minutes after the first failure. However, after the first execution the 

### Call On

The `Call On` field is used to specify whether a reaction should be executed on Healthy or Failed monitors. Not all reactions have this setting as some reactions only apply to Failed or only apply to Healthy monitors.

