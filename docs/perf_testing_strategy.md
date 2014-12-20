

Performance testing strategy
============================

# Introduction

There are two aspects regarding Runbook performance testing:

- operations performance testing
- backend engine performance testing

Operations performance testing addresses the performance concerns about the website facilities as well as overall service performance.

While the Backend  engine performance testing addresses the performance concerns about the intrinsic behavior of the monitor/reaction facility.

# Ops testing 

[Locust](http://locust.io) appears as a good component of a successful Ops testing strategy since, it supports:

- \>10k simultaneous users simulation load testing 
- summary statistics per url
- python based test writing 
- distributed load testing
- failure status

This covers load testing mostly at the QA level, since it is typically fired at pre-deployment.

In post-deployment, we need to cover these additional aspects:

- live (non incapacitating) performance testing
- ops performance testing monitoring - keeping track of changes to the response times of various facilities covered by load testing

These can be covered by a regular monitoring system than can both:

- feed on Locust result
- feed on its own website testing service

Two approaches appear then:

- adding such a fonctionality to Locust - but this could possibly bloat it --> _cf._ the KISS principle
- interfacing with existing monitoring solutions:
    + simple : [Munin](http://munin-monitoring.org/), [StatsD](https://github.com/etsy/statsd) + [Graphite](https://github.com/graphite-project/graphite-web)
    + full blown : [Zenoss](http://zenoss.org)


# Monitor/Reaction testing

Although this topic is not exclusively performance related, it is critical to the design of the Monitor/Reaction performance testing.

## The Testing Framework
This requires setting up the test case environment. Once it is up, the testcase requires:

- being able to test if some service is up or down (some simple script that speaks to the service) and exits with a success or failure return code. This is the monitor.
- a breaker script that either kills the service, fills disk space or anything else, depending on the test case scenario and reaction capabilities
- The reaction

These three components would interact in the follow sequence:

1. The service starts (using a docker configuration)
1. The monitor checks it is running (manually run)
1. The breaker does its thing
1. The monitor checks it is not running anymore (manually run)
1. The reaction runs
1. The monitor checks it is running (manually run)

Another type of testcase would be doing the same thing with Runbook running. Only step `5`. changes to:

- (bis) Runbook starts and checks the service using both the monitor and the reaction


## The testcase environment

Environments can be set using [vagrant](https://www.vagrantup.com/) + [docker](https://www.docker.com/) (as a Provider) for prototyping the test cases (and also our dev tasks), and then either:

1. aws/openstack + docker (with almost no code change). Integration to a CI (Jenkins, Travis-CI) would then be straightforward
1. use performanceci ( https://github.com/performanceci/performanceci-core ) on a hosted testing VM
1. use http://performanceci.com (hosted solution) when it's launched and the pricing is right

Item 2 seems to be the way to go, since it's a full CI and the docker testing environment we set up would be directly used in performanceci. The latter requires a `Dockerfile` and a `perfci.yml` (obviously :-).


## The testcase generator

This feature won't be needed immediately, but as soon as (or before) testcase writing becomes cumbersome, we could use a testcase generator:

- we would only define the setup and teardown proc (some service specific testing environment Dockerfile)
- the breaker script(s) would incur an anomaly of some kind
- the monitor/reaction would have to find and correct the flaw

The generator would create a test case for each `service x monitor x reaction x anomaly`.

# Monitor/Reaction performance testing


## Monitor performance testing

Monitors run frequently waiting for an event to trigger status change. As such, a monitor needs to return a status in a __reasonable__ time, _i.e._ a time the monitor developer or user considers to be acceptable.

Monitor performance testing would require setting different thresholds for each monitor.


## Reaction performance testing

Reactions are run once after a monitor status trigger event. Similarly to monitors, reactions performance evaluation depends on developer and user requirements.

# Summary

The suggested tools would be:

- [PerformanceCI](https://github.com/performanceci/performanceci-core) (self hosted or externally hosted)
- [Locust](http://locust.io)
- [Docker](https://www.docker.com/)
- [Vagrant](https://www.vagrantup.com/) (with Docker as a provider)

This would provide us with full performance testing with :

1. performance testing development
1. provisioning
1. CI

We will lack performance regression detection (service would be slower but still faster than threshold). This would require custom developments as shown on  `Ops testing`.

