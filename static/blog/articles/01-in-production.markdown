---
author: Benjamin Cane
authorlink: https://twitter.com/madflojo
date: 2014-07-08 07:00:00+00:00
pubdate: Tue, 08 Jul 2014 07:00:00 -07:00
popularity: None
slug: now-in-production-and-a-ton-of-new-features
title: "Now in production, and a ton of new features"
description: CloudRoutes is officially out of beta, and from now on we are focused on building a system that fixes issues for you. Especially at 3 in the morning.
post_id: 1
categories:
- Announcements
- Engineering
tags:
- DevOps
- DevOps incidents
- Automated incident mitigation
- DNS Failover
- Automated resolution
---

When we launched CloudRoutes in April our plan was to go into production the next month. While it may have taken us a month or two longer than we planned, we are happy to announce that today we have migrated our platform from Beta to Production. As promised any Beta users that had signed up for a paid subscription will be able to keep their current beta subscription plans, however new users will be offered our production pricing plans.

This announcement however is for more than our move from Beta to Production. We have also released a new version of our platform today, and that version comes with quite a few new features.

## New Features

### Monitors and Reactions

When we initially launched our platform we gave our users the ability to monitor a TCP Port and if that port was not responding we would automatically remove the failed IP from CloudFlare's DNS. With our latest release we have changed the design of how this all works. The latest version of our application has two components [Monitors](https://cloudrout.es/monitors) and [Reactions](https://cloudrout.es/reactions). Monitors, are designed to keep an eye on your applications or servers. Reactions, are sets of actions that are performed when the monitors have failed.

#### Monitors

With this new release we have added several new monitors to help keep an eye on your applications and servers.

##### HTTP/S GET Status Code

The HTTP/S GET status codes monitor is designed to allow you to monitor the HTTP status codes your application returns. With our implementation of this monitor you can customize which status codes are good and which status codes are bad.

##### Webhook API

The Webhook API monitor can be used to integrate our reactions into your existing monitoring and management tools. Our API is a simple JSON REST API and can easily be integrated into custom scripts. We also give you the ability to setup multiple API end points, this allows you to setup different reactions for different end points.

##### Datadog Alerts

Our goal is to provide you with the tools to automatically resolve issues. While we offer monitors to help make this happen at the end of the day we are not looking to replace other monitoring tools but rather work with those tools to provide automated resolution and mitigation. One of the first monitoring services we decided to integrate with is Datadog. Using the Datadog Alerts monitor you can trigger reactions on anything that Datadog monitors.

#### Reactions

In our previous release we didn't have the concept of reactions, we only performed one task when a monitor failed. In this release however we have added the ability to customize what reactions are executed when monitors fail. We also have given you the ability to attach multiple reactions to a single monitor.

##### Remove an IP from DNS (CloudFlare)

This reaction was once the single purpose of our platform, and we still feel it is very necessary. Using this reaction you can setup Round-Robin DNS Load Balancing with CloudFlare and use any or all of our monitors above to remove unhealthy web servers. One caveat to this monitor is that it will not remove an IP from DNS if it is the only IP for that specific record. This is designed to prevent complete outages if multiple servers are failing their monitors but not completely down.

##### Replace an IP in DNS (CloudFlare)

This reaction was designed for systems that cannot use Round-Robin DNS but still need failover. One could use this reaction for failing over Master - Slave replicated applications or any system that required Active-Passive failover. Most reactions have an action that is performed when the monitors return healthy and a different action when the monitor returns failed. This monitor however does not, this monitor only performs an action for failed monitors. This is to prevent flapping situations where a monitor is failed, then healthy, then failed again. We feel that it is better to fail back manually when using Active-Passive failover.

##### Email Notification

This reaction is pretty straight forward, it allows you to send yourself a notification whenever a monitor changes it's status from failed to healthy or healthy to failed. In the past we would send email notifications to the email account on file; however this monitor allows you to send the email to any email address. This can be used to integrate our monitors with systems such as PagerDuty, BigPanda or anything else that accepts emails. 

##### StatHat Statistics

Want a graph of how many times your servers were down? Or do you want a graph of the number of times your web server returned a `500` error code. With our StatHat reaction you can do just that. This reaction will use the StatHat API to send custom statistics to StatHat. This reaction will send either Value stats or Counter stats and we give you the option to send them when the monitor returns healthy or when it returns failed.

### Manual monitor actions

In addition to Monitors and Reactions we also added the ability to mark any monitor failed or healthy through the dashboard. This will allow you to test your reactions without the monitors actually failing. If your monitors have DNS failover reactions associated you could potentially use the manual actions to take a server out of service without impacting existing traffic.

### CloudRoutes API for all non-API based monitors

Some monitors such as the Datadog Alerts monitors are managed by API calls from third party applications, other monitors such as TCP Port check are non-API based. As part of this release we have taken the CloudRoutes Webhook API and made it available for the other non-API based monitors. This allows you to change the status of monitors through custom tools or other third party systems that are not currently supported.

### A Blog

Another new feature to be announced today is the addition of this blog, which you are most likely reading this post from. This blog will be used for announcements, tutorials or any other engineering type of posts. You can follow our [RSS](http://feed.cloudrout.es) or [Twitter](https://twitter.com/cloudroutes) feeds for the latest and greatest posts. 

### Modularity

While this last new feature may not be as visible as the others we feel that this is the most important feature of them all. For the past few months we have been spending countless hours re-coding our application to allow us to quickly add new monitors and reactions. We feel that by making our system more modular we can add new functionality quicker and eventually allow our platform to provide more than just DNS failover.

## Thanks to the Beta Users

As a final note I wanted to say thank you to our Beta users, we received some great feedback from you and have tried to capture all that we could with this release. It is also important for you to know that any domains/health checks you had added in our old system has since been migrated to our new version. If you have any issues with your migrated monitors you can contact us at support@cloudrout.es
