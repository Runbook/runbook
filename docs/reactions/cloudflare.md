The CloudFlare Reactions are designed to provide DNS failover for [CloudFlare](https://www.cloudflare.com/) protected domains.

## TTL

It is recommended for DNS Reactions to keep the TTL of each record hosted with CloudFlare set to Automatic. The automatic setting will allow CloudFlare's reverse-proxy servers to detect the change immediately, making the modification faster.

---
## Remove an IP

The **CloudFlare DNS: Remove an IP** Reaction is designed to provide an Active-Active DNS Failover functionality for domains that host their DNS with CloudFlare. This Reaction is mainly useful for domains utilizing round-robin DNS load balancing. DNS records that are removed during a false reaction are stored in Redis. When the Monitor that triggered the removal of DNS is restored to a true state, the DNS records are re-added automatically.

**Note:** This Reaction will not remove any records that do not have a secondary entry. For example, consider a scenario where you have two `www` records, one pointing to `10.0.0.1` and another pointing to `10.0.0.2`. If the Reaction was configured to remove `10.0.0.2`, it would. If a second Reaction was then told to remove `10.0.0.1`, then our system would do nothing. This is designed to prevent a complete outage when issues may be occurring on both systems but are not impactful enough to completely take the system offline. It is generally better to route incoming traffic somewhere even if that system is not completely true.

When re-adding DNS records, secondary parameters such as `prio` for `MX` records and `service_mode` for `A` records are re-added with the same settings as when they were removed.

---

## Replace an IP

The **CloudFlare DNS: Replace an IP** Reaction is designed to provide Active-Passive DNS failover for domains that host their DNS with CloudFlare. This Reaction can be used to provide DNS failover for systems that cannot run in an Active-Active state.

An example of this could be databases. Some databases support Master-Master replication. However, this replication strategy can cause conflicts when both systems are being written to at the same time. This Reaction could be utilized to direct traffic to only one Master server and if any associated Monitor fails this Reaction can replace the first Master server's IP with the second Master server's IP.

### Failback Method

The Reaction creation form for **CloudFlare DNS: Replace an IP** contains a select field that allows you to choose either `automatic` or `none`. The `automatic` failback policy will cause the Reaction to re-add removed records when the Monitor that triggered the Reaction returns a true state. The `none` failback policy will cause the Reaction to perform no action when the triggering Monitor returns a true state.

---