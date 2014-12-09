This document explains the architecture of Runbook; this guide is useful for Developers looking to contribute to Runbook as well as anyone else interested in the setup and design.

---

## Principles of Runbook's Architecture

Before explaining the components of the Runbook application it is important to cover the key principles that govern architecture decisions for Runbook. You can think of these as Runbook's rules of architecture.

#### Be highly available

While Runbook currently does not offer an SLA for availability to it's users high availability is a key component of it's design. Our users rely on Runbook to resolve issues automatically for them during their own outages, if our monitoring service is unavailable to them while they are having an outage we are not going to continue having their trust.

#### Our monitoring service is more important than our dashboard

While it might sound counter intuitive to our first principle, with high availability comes choices. If a design must choose between the availability and function of the web interface vs the availability and function of our monitoring service. The monitoring service should come first. Obviously, every effort should be made to maintain the availability of the web interface but this is secondary to our monitoring system. An example of this decision can be seen in the way our reaction processes handle database downtime.

#### Each component must be able to scale

When designing and developing for Runbook it is important to think about the scale of the changes your making. Can these changes being made scale to thousands of users with thousands of monitors. Could Facebook or Google use our product out of the box? With this in mind we tend to keep monitors and reactions as stateless as possible and only utilize our Redis Cache and RethinkDB database for only what is required to perform the action. Sometimes however we do need to store data for monitors and reaction states; when we do that data is stored in Redis with a timeout value. Ensuring that even if we need that data it is only the latest data we need and will be purged automatically to avoid data bloat.

#### Encrypt network communications between servers

While the application itself does not always encrypt communications (due to the complexity of encryption and key exchanges). The traffic itself is encrypted when it leaves the server. Runbook heavily utilizes stunnel, an example of this is that our data persistence layers do not inherently support encryption. So all client and server communications are tunneled through stunnel.

#### Do not assume any network is trusted

The encryption methods above are used even for servers that exist in the same datacenter. DigitalOcean and many other providers generally offer a private network however, this network should not be assumed as private since other customers of DigitalOcean also have access to it.

#### Keep it simple and stupid

While this is a bit of a difficult thing to follow when developing a complicated system such as Runbook. Sometimes a developer may find themselves faced with a decision to build a component with simplicity in mind or functionality in mind. It is often better to design with simplicity, as simplicity will allow for a greater addition of functionality later. In addition, simplicity makes the production system easier to manage and easier to manage automatically.

#### Be modular

The Runbook application is designed to be modular as possible, and places where it is not are under development to improve their modularity. By keeping the application modular we are able to add features faster and simpler. New developers are able to add functionality without knowing and understanding the full application.

#### Eat your own dog food

Runbook is a service that allows users to build environments that require minimal human interaction, especially for incidents. Runbook heavily relies on it's own application to provide a "self healing" environment. This is part of the reason that the monitoring service must be kept available above the web interface. When the web interface goes down, the monitoring service can correct it. Runbook has no on call support, and this requires Runbook itself to be it's own most advanced user.

---

## Components

Runbook currently has 4 major application components, `monitors`, `cras`, `crbridge` and `web`. Each component is designed to be independently scalable. One component may be scaled without requiring other components to meet the same scalability.

**Note:** The name CloudRoutes will appear several times within this document, this is because it is the original name of the Runbook product.

### WEB  - CloudRoutes Web Application

The CloudRoutes Web Application is the easiest component to understand. This is a simple Flask web application that serves as the user interface for creating monitors and reactions, managing a users subscription, and a dashboard for the current state of monitors. In addition the WEB component also receives and processes webhook monitors. These are monitors where outside services such as Datadog, PaperTrail or Travis-CI notify Runbook of monitor status.

The main process for this application is `web.py`. In production this process is managed by the `uWSGI` application server, which is launched via `supervisord`. The `supervisord` service will restart the `uWSGI` processes should they fail or be stopped abnormally.

In front of the `uWSGI` process is the `nginx` webserver. This webserver is used to serve static files and forward non-static requests back to the `uWSGI` service. This design is also designed to scale as needed. It is possible to run more `uWSGI` back-end application servers than `nginx` front-end webservers. At the moment these are in a one to one ratio but could be changed easily.

#### Persistence

WEB uses RethinkDB as it's back-end database system. [RethinkDB](https://rethinkdb.com) is a highly scalable JSON document database. We choose this database for several reasons.

1. It provides out of the box synchronous replication
2. Queries are automatically parallelized and distributed amongst multiple nodes
3. Allows for scaling at both a local datacenter and cross datacenter level

### CRBRIDGE - CloudRoutes Bridge

The CloudRoutes Bridge application is designed to bridge the gap between the web front-end and the monitoring and reacting back-end systems. When monitors and reactions are created the WEB process stores them into the `monitors` or `reactions` tables within RethinkDB; the WEB process also places a `create`, `edit`, or `delete` entry into the `dc#queue` tables within the database. The `crbridge/bridge.py` process is constantly reading from the `dc#queue` table and processing the entries placed within those tables.

Each `dc#queue` table is unique for each datacenter Runbook runs from. In production today Runbook runs out of only 2 data-centers, this means currently there are two `dc#queue` tables. `dc1queue` and `dc2queue`. Since the WEB process itself does not interact with the back-end monitors the `dc#queue` tables are used to relay tasks to the back-end systems. It is the `crbridge` systems responsibility to process those tasks.

When the `crbridge` process receives a `create` task it will read the monitor or reaction configuration from the database entry and store that data in that data-centers local Redis instance. Each datacenter or "monitoring zone" within the Runbook environment has it's own local Redis server. This Redis server is not replicated to any other data-centers and is simply there to serve as a local cache for monitors and reactions running from that datacenter.

**Note:** If an issue was to occur where a local Redis instance was destroyed and unrecoverable a new Redis server can be repopulated using the `crbridge/mgmtscripts/rebuild_Redis.py` script. This script reads from RethinkDB and creates edit requests within each data-centers `dc#queue`. This will cause a re-population of each Redis instance in each datacenter. This is a benign process as RethinkDB is designed to be the source of truth regarding monitor and reaction configurations.

In addition to creation and deletion tasks the WEB will also writes webhook monitor events to the local `dc#queue`. If the WEB instance is running in datacenter 1 it will write to the `dc1queue`. When the bridge process identifies a monitor event it will forward an even JSON message to the `cras/broker.py` process. Again, acting as a bridge between the web application and the back-end monitoring application.

Recovering from RethinkDB failures, when RethinkDB servers are experiencing issues in it's current configuration the RethinkDB instance may become read only until the other nodes are automatically recovered. During this time being read only monitors and reactions are unable to write historical logs of execution. During this time those processes will write those logs to Redis. When the bridge process is starting it will read the Redis keys associated with these logs and if there is data it will process them and store them into RethinkDB; essentially becoming a write behind process.

#### Diagram showing monitor creation process

![Monitor Creation](/img/architecture/monitors-creation-multidc.png)

#### Diagram showing reaction creation process

![Reaction Creation](/img/architecture/reaction-creation-multidc.png)

### MONITORS - CloudRoutes Availability Monitor

The CloudRoutes Availability Monitor component is designed to perform the actual monitoring of remote systems. This is the monitoring part of the monitoring and reacting back-end application. This component is comprised of 3 major programs `control.py`, `broker.py`, and `worker.py`.

#### Control

When the CloudRoutes Bridge process adds monitor details into Redis it looks at the monitor details and extracts the `interval` value. This `interval` key is a queue, the monitors ID number is added to this queue which is essentially a sorted list within Redis. The interval defines how often the monitors should be executed, in production today there are 4 valid intervals.

* `30mincheck` - This sorted list is for monitors that run every 30 minutes
* `5mincheck` - This sorted list is for monitors that run every 5 minutes
* `2mincheck` - This sorted list is for monitors that run every 2 minutes
* `30seccheck` - This sorted list is for monitors that run every 30 seconds

The `monitors/control.py` program is a generic program that is designed to pull monitor IDs from a defined sorted list in Redis (one of the intervals listed above). Once it has a list of monitor IDs it will loop through that list and look-up the monitors details from Redis using the monitor ID as a key. Once the monitors details are read, the `monitors/control.py` process will create a JSON message including the monitors details and send that message to `monitors/broker.py` using ZeroMQ.

Each `monitors/control.py` process can only read from one sorted list, in order to have all sorted lists monitored each sorted list must have it's own `monitors/control.py` process. This is possible as the `monitors/control.py` process receives all of it's Redis and timer configuration from a configuration file. In production there are currently 4 `monitors/control.py` process running per datacenter.

#### Broker

The `monitors/broker.py` or MONITORs Broker process is simply a ZeroMQ broker. The process binds two ports, one port is used to listen for ZeroMQ messages from the various `monitors/control.py` processes. The second port is used to send that received message to a `monitors/worker.py` process. Currently in production each datacenter has only 1 MONITORS Broker, however this process is not limited to only one. When two servers are specified in an stunnel configuration the stunnel service will send requests in a round robin algorithm. This allows the control messages to be sent to multiple brokers which then could be sent to multiple sets of workers.

#### Worker

The `monitors/worker.py` or MONITORS Worker process is the actual process that performs the monitor tasks. The code to perform an actual monitor check is stored as modules within `checks/` directory. For example, TCP Port monitor is the module `checks/tcp-check`. When the MONITORS worker process receives a health check message from the MONITORS Broker it decodes the JSON message and determines what type of check module should be loaded. It then loads the module and executes the `check()` function passing the monitor specific data to the function.

The `check()` function will return either `True` for true or `False` for false. With this result the worker process will generate a JSON message which is then sent to the CloudRoutes Action Service.

#### Diagram showing monitor execution process

![Monitor Execution](/img/architecture/monitor-execution.png)

The entire CloudRoutes Availability Monitor design is built to scale. The Worker processes are design to run in large numbers, currently in production each monitoring zone is running approximately 25 worker processes. The Broker facilitates this, by having each Control process route though the Broker we are able to fully utilize each worker process and able to distribute monitor executions efficiently. The Control processes are the only singleton, but these processes are unique for each monitoring zone. It is simple enough to add monitoring zones as needed, if the performance of the Control process is unable to keep up with demand the answer is to simply add additional monitoring zones.

### CRAS - CloudRoutes Action Service

The CloudRoutes Action Service or CRAS is designed to perform the "Reaction" aspect of Runbook's Monitoring and Reacting. Like the MONITORS there are two main programs with CRAS, `cras/broker.py` or CRAS Broker and `cras/actioner.py` or CRAS Actioner.

#### Broker

Like the MONITORS Broker the CRAS Broker simply receives JSON messages from the MONITORS Worker or CRBRIDGE Bridge processes and forwards them to a CRAS Actioner process. This facilitates the ability for multiple monitor results to be processed at the same time and from multiple machines. Like the MONITORS broker while currently this process is a single process in each datacenter it does not necessarily require this. To scale the performance of monitor result processing multiple Brokers could be launched.

#### Actioner

The CRAS Actioner process is the process that performs reaction tasks. Like the MONITORS worker the code to perform a reaction is stored within modules in the `monitors/` directory. An example of this would be the `monitors/enotify` module which handles email notification reactions.

When the CRAS Actioner process receives the JSON message from the MONITORS Worker process it will first look-up the monitor from Redis and then RethinkDB. If the RethinkDB request does not return a result due to a RethinkDB error the monitor is flagged as a `cache-only` monitor. The idea behind this is that even if RethinkDB is down the monitor should still be actioned to ensure that Runbook is providing it's function of protecting user environments.

Each monitor JSON message has a list of reactions associated with that monitor. After looking up he monitor the Actioner process will loop through these reactions. The Actioner will look-up reaction details first from Redis and secondly from RethinkDB following the same process as the monitor data look-ups. In this case, the Actioner will compare the `lastrun` time from both results and utilize the newest. This is to ensure that `frequency` settings within the reaction are honored if the reaction was executed from another datacenter.

When the Actioner process has the reaction data it then loads the appropriate `monitors/` module and executes the appropriate method for performing the reaction. When reactions are executed a set of "meta" reactions are also executed, these are essentially reactions of reactions and are used to update the RethinkDB and Redis datastores as well as update any reaction tracking logs.

After all user defined reactions have been executed a list of default reactions are executed for the monitor. These reactions are similar to the "meta" reactions, but are reacting on the monitor itself rather than the reaction.

#### Diagram of reaction execution

![Reaction execution](/img/architecture/reactions-execution.png)

## Architecture Diagrams

Below are links to Architecture Diagrams of the Runbook environment, each of these diagrams show a different aspect of Runbook's application environment.

* [Component Overview](/img/architecture/overview.png)

This shows a holistic view of each component and it's interactions. This also depicts a typical development environment setup, you can think of this as the minimal required implementation.

* [High Availability Deployment](/img/architecture/overview-multidc.png)

This diagram depicts each component and it's interactions as it is deployed in two data-centers. When considering this deployment it is feasible for Runbook to be deployed across more than two data-centers.

* [High Availability and Scalabitlity Deployment](/img/architecture/overview-scaledandredundant.png)

This diagram shows each component deployed in a highly scaled out and redundant design. Components with multiples can be scaled beyond the number depicted as needed, components without multiples such as the control.py processes can expanded by adding additional monitoring zones. The CRBRIDGE Bridge component in theory could support running multiple copies however this is untested at this time.


---
