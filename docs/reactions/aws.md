# Amazon Web Services (AWS)

The Amazon Web Services reactions are designed to allow the user to interact with AWS instances and eventually other AWS services.

---

## Restart Instance

The Restart Instance reaction allows users to restart AWS EC2 instances. This reaction can be used as a last resort when all other reactions failed to resolve the issue.

---

## Stop Instance

The Stop Instance reaction allows users to stop AWS EC2 instances. This reaction has a bit of an edge case but could be used to stop instances that have a limited use.

---

## Start Instance

The Start Instance reaction allows users to start AWS EC2 instances. This reaction has a bit of an edge case but could be used to start an instance that is designed to take over from another failed instance. Using this reaction along side the CloudFlare DNS: Replace IP reaction, one could build a Active - Standby failover that is initiated and performed automatically.
