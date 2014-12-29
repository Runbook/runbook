[Commando.io](https://commando.io) is a SaaS product that allows you to execute commands/scripts called "Recipes" across any number of servers. It provides a web interface for running commands and allows its customers to give an audit-able access to users by allowing them to execute specific commands on specific servers.

Commando also has an API that allows paid users to execute Recipes via API calls. These Runbook Reactions utilize this same API and thus require a paid account with Commando.

---

## Execute Recipe (Single Server)

The **Commando: Execute Recipe (Single Server)** Reaction allows users to execute specified Commando recipes on a single server. A great use case for this reaction would be to restart a database service if it has crashed.

---

## Execute Recipe (Group of Servers)

The **Commando: Execute Recipe (Group of Servers)** Reaction allows users to execute specified Commando recipes on a group of servers. A great use case for this Reaction would be to have Commando run a Saltstack highstate or Puppet agent run when a Monitor is triggered.

### Group ID

The Group ID field accepts a comma separated list of group IDs, giving the user the ability to request a recipe execution on multiple servers with one Reaction.

---