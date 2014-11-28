# CloudFlare

The CloudFlare Reactions are designed to provide DNS failover for CloudFlare protected domains.

## TTL

It is recommended for DNS reactions to keep the TTL of each record hosted with CloudFlare set to Automatic. The automatic setting will allow CloudFlares reverse proxy servers to detect the change immediately making the modification faster.

## CloudFlare DNS: Remove an IP

The CloudFlare DNS: Remove an IP reaction is designed to provide an Active-Active DNS Failover functionality for domains that host their DNS with CloudFlare. This reaction is mainly useful for domains utilizing round-robin DNS load balancing. DNS records that are removed during a failed reaction are stored in Redis. When the monitor that triggered the removal of DNS is restored to a healthy state the DNS records are re-added automatically.

**Note:** Our reaction will not remove any records that do not have a secondary entry. For example, if you had two `www` records; one that pointed to `10.0.0.1` and another that pointed to `10.0.0.2`. If the reaction was configured to remove `10.0.0.2` it would. If a second reaction was then told to remove `10.0.0.1` than our system would do nothing. This is designed to prevent a complete outage when issues may be occurring on both systems but are not impactful enough to completely take the system offline. It is generally better to route incoming traffic somewhere even if that system is not completely healthy.

When re-adding DNS records secondary paramaters such as `prio` for `MX` records and `service_mode` for `A` records are re-added with the same settings as when they were removed.

---

## CloudFlare DNS: Replace an IP

The CloudFlare DNS: Replace an IP reaction is designed to provide Active-Passive DNS failover for domains that host their DNS with CloudFlare. This reaction can be used to provide DNS failover for systems that cannot run in an Active-Active state.

An example of this could be databases; some databases support Master-Master replication however this replication strategy can cause conflicts when both systems are being written to at the same time. This reaction could be utilized to direct traffic to only one Master server and if any associated monitor fails this reaction can replace the first Master servers IP with the second Master servers IP.

### Failback Method

The reaction creation form for **CloudFlare DNS: Replace an IP** contains a select field that allows you to select either `automatic` or `none`. The `automatic` failback policy will cause the reaction to re-add removed records when the monitor that triggered the reaction returns a healthy state. The `none` failback policy will cause the reaction to perform no action when the triggering monitor returns a healthy state.
