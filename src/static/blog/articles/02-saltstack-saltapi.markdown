---
author: Benjamin Cane
authorlink: https://twitter.com/madflojo
date: 2014-07-28 08:00:00+00:00
pubdate: Mon, 28 Jul 2014 08:00:00 -07:00
popularity: None
slug: using-saltstack-and-cloudroutes-to-automagically-fix-issues-at-3-am
title: "Using SaltStack and CloudRoutes to automagically fix issues at 3 A.M."
description: CloudRoutes has recently added SaltStack based reactions utilizing salt-api. These reactions allow you to automatically fix issues as soon as they are detected.
post_id: 2
categories:
- Announcements
- Engineering
tags:
- DevOps
- DevOps incidents
- Automated incident mitigation
- DNS Failover
- Automated resolution
- SaltStack
- salt-api
---

In our last blog post we eluded to the fact that we have been planning on adding features that go beyond the scope of DNS failover. Today's release does just that. 

## Integrating with SaltStack

Performing DNS failover when monitors detect issues is great, it keeps end users from being impacted by the issue at hand. The problem with only performing DNS failover is that someone still has to wake up in the middle of the night to resolve the issue that caused the failover in the first place. 

That is where our new SaltStack Reactions come into play. Today we deployed several SaltStack based reactions that allow you to fix those middle of the night issues automatically, without having to even pickup the phone.

### How it works

We covered this quite a bit in our previous posts but for anyone new it is important to first understand how CloudRoutes works. Our whole platform is dedicated to providing a system that allows you to automatically resolve issues. To do this we have two components; **Monitors**, which are used to keep an eye on applications or servers and **Reactions**, which perform the heavy lifting of resolving those pesky 3 a.m. problems.

With this release we have deployed several **Reactions** that allow you to initiate SaltStack executions. We do this by integrating with **salt-api**; SaltStack's web based api system.

#### salt-api

The **salt-api** project was merged into the main Salt repository with the release of SaltStack Helium. **salt-api** is a REST API that allows you to execute Salt modules via web requests. This allows you to integrate third party services (like us for example) with your configuration management system.

For us, this means giving us an interface to run actions that resolve issues rather than simply working around them.

### New Reactions

Because **salt-api** allows you to perform many tasks we decided to keep our reactions as flexible as possible. We have added several reactions that provide you with specific tasks such as Restarting nginx, or Executing a script but we have also provided a reaction that is flexible enough to run most SaltStack modules. You can check out our [Available Reactions](https://cloudrout.es/reactions/) page for a full list of reactions.

### Some assembly required

While **salt-api** is great and allows us to interact with SaltStack very easily, it does require some [setup and configuration](http://bencane.com/2014/07/17/integrating-saltstack-with-other-services-via-salt-api/). We have created a [GitHub Repository](https://github.com/CloudRoutes/integrations/tree/master/saltstack/salt-api) with several templates that can be used with our reactions.

These templates are used to define what can be executed via **salt-api** and they are designed to work with our new reactions. The templates are also generic enough to use with services other than CloudRoutes as well, feel free to take these templates and use them to integrate your own systems with SaltStack. We only ask if you have any suggestions or modifications to contribute back so that others can use them as well.

### What about Puppet, Chef, cfEngine, Ansible or anyone else

You might be asking why we chose to integrate with SaltStack vs. some other configuration management and automation tool. The answer simple.

1. SaltStack has an API **(salt-api)** that allows us to integrate in a very flexible way, and the others that we looked at didn't or we couldn't find it.
2. We use SaltStack... So this helps us rest through the night as well.

If you use one of the other guys, don't worry. We are continuing to look at ways to integrate with all of the major players in the infrastructure automation space. If they don't offer an easy to use API, we have other ways...
