Unlike other Reactions that simply work with other services out of the box, [Saltstack](https://www.saltstack.com/) is not run as a service. Typically Saltstack would be deployed within your own organization. This means that some setup is required in order to utilize these Reactions.

---

## Salt API & Reactor Formula

The Runbook Saltstack Reactions are based on the [Salt API & Reactor Formula](https://github.com/madflojo/salt-api-reactor-formula), which is a Saltstack formula that can be easily deployed. Outside of deployment no other configuration is required.

---

## Manage Services

The **Manage Services** Reaction is designed to allow users to `start`, `stop`, `reload` and `restart` services across one or many servers using Saltstack. This Reaction is extremely practical as it allows users to restart false services.

---

## Manage Minion Keys

The **Manage Minion Keys** Reaction is designed to allow users to `accept`, `delete` or `reject` minion keys within Saltstack. This Reaction could be combined with provisioning and deprovisioning actions to programatically accept new minions.

---

## Execute a Command

The **Execute a Command** Reaction is designed to allow users to execute arbitrary commands across one or many servers using Saltstack. This Reaction is useful for combining legacy scripts for system health with Runbook's monitoring.

---

## Initiate a Highstate

The **Initiate a Highstate** Reaction is designed to allow users to execute a Saltstack highstate across one or many servers using Saltstack. This Reaction is useful as it can be used as a general purpose Reaction. It provides users with a quick and easy way to ensure their infrastructure is in the correct state, as defined by Saltstack.

---

## Run a Script

The **Run a Script** Reaction is designed to allow users to tell Saltstack to download a script from a remote location and execute it on the servers specified. This Reaction is similar to the **Execute a Command** Reaction except that it allows users to download the command to execute from a remote HTTP or Saltstack file server.

---

## Execute a Module

The **Execute a Module** Reaction is designed to allow users to execute any Saltstack module across one or many servers. This Reaction is a general purpose Saltstack Reaction, it can be used to call any and all modules defined within Saltstack.

---