[Commando.io](https://commando.io) is a SaaS product that allows you to execute commands/scripts called "Recipes" across any number of servers. It provides a web interface for running commands and allows it's customers to give an auditable access to users by allowing them to execute specific commands on specific servers.

Commando.io also has an API that allows paid users to execute Recipes via API calls. The Runbook reactions below utilize this same API and thus require a paid account with Commando.

---

## Execute Recipe (Single Server)

The Commando: Execute Recipe (Single Server) reaction allows users to execute specified Commando.io recipes on a single server. A great use case for this reaction would be to restart a database service if it has crashed.

---

## Execute Recipe (Group of Servers)

The Commando: Execute Recipe (Group of Servers) reaction allows users to execute specified Commando.io recipes on a group of servers. A great use case for this reaction would be to have Commando.io run a saltstack highstate or Puppet agent run when a monitor is triggered.

### Group ID

The Group ID field accepts a comma seperated list of group id's, giving the user the ability to request a recipe execution on multiple servers with one reaction.
