CloudRoutes
===========

CloudRoutes is a Software as a service with the goal of eliminating the need for Development & Operations On Call. We will accomplish this by providing solutions to monitor applications and infrastructure; when our **Monitors** detect failure our platform will initiate predefined automatic responses. Ideally these responses called **"Reactions"** will automatically resolve the underline issue eliminating the need to alert the On Call Developer/Sysadmin/DevOps person.

By automatically resolving production issues our system will enable users to focus on finding the root cause of reoccuring incidents rather than fighting day to day fires.

A few examples of the types of activities that CloudRoutes can perform today are.

* Perform DNS changes to failover traffic
* Reboot Digital Ocean or AWS servers
* Perform SaltStack WebAPI calls to execute scripts or commands
* Send a notification email (Worst case scenario)
* Send Statistics to StatHat

## Parts of this project

### crweb - CloudRoutes Web Interface

This section is the web interface for CloudRoutes. This is the meat and potatoes of the web interface used by users, it allows users to create and manage Monitors and Reactions as well as provide a dashboard to identify what monitors are healthy, or failed. This is also the receiver of API based monitors such as the Datadog Webhook integration and CloudRoute's API version 1.

### cram - CloudRoutes Availability Monitor

This section performs the actual monitoring of user created monitors. There are three main components to this system; **control**, **broker** and **worker** each of these components are used to perform and schedule monitor checks.

#### Control

The control component will read from a Redis slist queue that contains the ID's of monitors that should be checked. The control will take this list and pull the additional details of those monitors and format them into a JSON message. That JSON message is then sent to the broker via ZeroMQ.

#### Broker

The broker will bind two zMQ ports, one to receive messages from various control processes and one to send messages to multiple workers. When the broker recieves the control servers JSON message he simply forwards that message to a single worker. This is a way of distributing the laod of monitor checks across many many workers. When it comes time to scale this platform out brokers and workers do not necessarily have to exist on the same server.

#### Worker

The worker component does the actually health check. Depending on the "ctype" value of the JSON message the worker will load the module `checks/<ctype>` and execute the Check method. If the Check returns True the healthy check is Healthy and then forwarded to the sink, if it is False it is marked failed and forwarded to the sink.

### crbridge - CloudRoutes Web to Availability Monitor Bridge

The bridge section is used to both synchronize the Redis Cache and the RethinkDB database as well as perform the reactions as necessesary. This component is made up of two parts, the bridge and the actioner (sink).

#### Bridge

The bridge component is used to synchronize the redis cache and rethinkdb and vice versa. It is also used to send any web based actions as in API monitors or manual healthy/failed changes to the sink/actioner for actioning.

#### Actioner (AKA Sink)

The actioner also known as the sink is the component that performs the reactions based on the defined reaction id's listed in the JSON message. Each reaction is a module in the "actions" directory and is loaded dynamically based on the rtype value in the Redis Cache/RethinkDB Database. If the monitor is failed it will execute the failed method and if it is healthy it will execute the healthy method. If the reaction should be run (based on frequency and trigger values) is up to the individual reactions module. If the reaction returns a True status the reaction executed, if the reaction returns a False status the rection tried to execute but failed, if the reaction returns a None status it was simply skipped.

### static - Static Files for Web Interface and statically generated pages (i.e. Blog, Frontpage)

These are static files for the web gui, blog, documents, frontpage etc.

### How to contribute

The best way to contribute is to join us at our [Assembly Project](https://assembly.com/cloudroutes) once there you can create bounties, add tasks, add input, contribute code or simply say hi. The biggest and easiest parts to contribute are to the Monitor and Reaction modules as they are simple to code and have the biggest impact by adding new features to the product.

### How Assembly Works

Assembly products are like open-source and made with contributions from the community. Assembly handles the boring stuff like hosting, support, financing, legal, etc. Once the product launches we collect the revenue and split the profits amongst the contributors.

Visit [https://assembly.com](https://assembly.com) to learn more.
