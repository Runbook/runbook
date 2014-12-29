The Amazon Web Services Reactions are designed to allow the user to interact with [AWS](http://aws.amazon.com/) EC2 instances (and eventually other AWS services).

---

## Restart Instance

The **Restart Instance** Reaction allows users to restart AWS EC2 instances. This Reaction can be used as a last resort when all other Reactions fail to resolve the issue.

---

## Stop Instance

The **Stop Instance** Reaction allows users to stop AWS EC2 instances. This Reaction is a bit of an edge case but could be used to stop instances that have a limited use.

---

## Start Instance

The **Start Instance** Reaction allows users to start AWS EC2 instances. This Reaction is a bit of an edge case but could be used to start an instance that is designed to take over from another false instance. Using this reaction along side the **[CloudFlare DNS: Replace IP](cloudflare.md#replace-an-ip)** Reaction, one could build a Active - Standby failover that is initiated and performed automatically.

---