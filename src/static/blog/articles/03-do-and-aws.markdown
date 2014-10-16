---
author: Benjamin Cane
authorlink: https://twitter.com/madflojo
date: 2014-09-08 08:00:00+00:00
pubdate: Mon, 8 Aug 2014 08:00:00 -07:00
popularity: None
slug: rebooting-servers-when-they-are-sick
title: "Rebooting servers when they are sick"
description: Rebooting servers when they are unhealthy is usually a frowned upon approach, however when taken with the context of automated incident response. This last ditch effort can be preferable to waking someone up at night.
post_id: 3
categories:
- Engineering
tags:
- DevOps
- DevOps incidents
- Automated incident mitigation
- Automated resolution
- SaltStack
- salt-api
- Rebooting Servers
---

Traditionally when a server is experiencing service degradation the response is for someone to login and investigate the root cause of the issue. For the record, this is the best way to identify what the cause of the issue is and how to resolve it for the long term. There is a problem with the traditional approach however; the problem is that this approach requires admins to maintain the same sleep schedule as the servers.

## The Traditional on call model

As we all know, servers don't sleep. Therefore they can break at any point whether that is 3 in the afternoon or 3 at night. Waking someone up in the middle of the night to fix an ailing server is something we at CloudRoutes feel is unacceptable; and we are working on replacing that methodology. To get us closer to a full replacement of on call rotations for Admins and DevOps we have launched our new DigitalOcean and Amazon Web Services [reactions](https://cloudrout.es/reactions/). With these new reactions you can use our monitors to detect failure in your environment and if that failure is not resolved by other methods. You can restart or power off the affected server.

While the thought of automatically rebooting a server may make some stomachs churn; keep in mind that in some environments this is a perfectly acceptable method of resolving the issue. Environments such as ours for example can survive with a single server being rebooted. This is especially true when that server has been removed from service before the reboot is even initiated.

## Architected to react to failures

To better explain why we can sleep comfortably with servers being rebooted automatically we are going to examine our architecture a bit. CloudRoutes requires several types of servers to keep things running, one type of server that gets the most mileage is our webservers. We have multiple webservers in our architecture and these webservers are split across data centers to reduce the likelihood of an entire data center outage taking our service offline. We are also heavy believers in automation and are able to spin up a new webserver as we need it. If a single server was dead we could simply destroy it and have a new one up within minutes.

Being a monitoring service, we monitor our own servers pretty heavily. We monitor the service ports, we perform pings, we perform HTTP calls to check the status code and check page output for errors. We check many components of our webservers, if any of these monitors fail the first failure invokes a <b>CloudFlare: Remove IP</b> reaction. This reaction uses the CloudFlare API to remove the failed servers IP address from DNS. From that point, any action we perform on that server has no effect on our users.

If the failure persists on the 2nd failure we utilize the <b>SaltStack: Highstate</b> reaction to run a highstate on that server. If the issue was due to a service crashing this will usually resolve it pretty quickly. We also set the frequency of this monitor to kick off every 5 minutes. If by the 3rd failure the issue is not resolved we use the <b>SaltStack: Manage Services</b> reaction to restart the most common services used by our webserver; nginx and supervisor.

All of these reactions have a frequency timer that allows them to be run repeatedly until the issue is resolved. However, if by the 20th health check the issue is not resolved we use the <b>DigitalOcean: Power Cycle</b> reaction. This reaction has a frequency of every 20 minutes, so if the server comes back and the issue is still persistent the Highstate, Service restart and Power Cycle reactions will all keep triggering until service is restored.

Since we have multiple webservers, and losing a single webserver does not mean our service is down. If none of these reactions resolve the issue then our system simply repeats the cycle until someone comes into the office the next morning and resolves the issue.

## Not everyone can just reboot

While automatically rebooting the server works for us, that is because our architecture is designed to accept failures. This works for us, however we do recognize that not every environment is the same, and rebooting the server is not an option for everyone. Environments, that cannot simply rebuild a server if it's dead or live with a single server offline for 8 hours. In some environments (and we have worked in them) you simply have to wake someone up. If you oversee one of these environments don't worry we are working on new reactions and monitors that will give you the ability to sleep through the night as well.

Until then, hopefully our new reactions will help some get better sleep at night.
