# Using Runbook and Commando to monitor and automatically restart nginx

## Introduction

In this tutorial you will learn how to setup a Runbook recipe that will ensure the nginx service is always responding with a `200 OK` response code.

At the end of this tutorial you will have a recipe setup that performs the following tasks.

1. Monitor nginx with an HTTP GET request
2. If the request fails or does not reply with `200 OK` restart nginx by executing a predefined Commando recipe

## Pre-requisites

This tutorial assumes the following:

* You already have at minimum a free account on [Runbook](https://dash.runbook.io/signup)
* You already have an account with [Commnado](https://commando.io) that has API access (required for Runbook integration)
* You have already defined and connected the servers in question on Commando
    * If this step is not already complete you can follow this [walk-through from Commando](http://vimeo.com/73097569)
* You already have a Commando API Key generated and available
    * API Key generation instructions can be found on [the Commando.io API walk-through video](http://vimeo.com/107547330)

### Setting up the Commando Recipe

Before setting up the Runbook recipe we will need to first create a Commando recipe to restart nginx. Before moving forward first log into your [Commando account](https://commando.io/lookup.html).

To create the nginx restart recipe navigate to the Recipes page.

![Recipe link](img/usertuts/http-commando-recipe/recipe.jpg)

Once on the recipe page click the **Add Recipe** button, after the page loads page you will be taken to a page where you can input the recipe. You can make a recipe that executes any type of script or command. For our example we will use the following command.

    # /usr/bin/sudo /etc/init.d/nginx restart

After filling out the form simply click **Add Recipe** again.

![Create Recipe](img/usertuts/http-commando-recipe/create-recipe.jpg)

The Commando recipe used for this example to restart nginx is a public recipe and can be found [here](http://public.recipes/4euvOE). 

## Creating a Commando Reaction on Runbook

For this section you will need to be logged in to both the Commando and Runbook dashboards. This section will guide you through creating a Runbook reaction that causes Commando to execute a Recipe on a defined server.

### How the Commando Execute Recipe Reaction works

This reaction works by sending an API request on your behalf to Commando. This reaction will take the API Key, Server ID and Recipe ID provided and send an API request to Commando. The request will tell Commando to execute the specified recipe on the specified server.

### Reaction Creation

Once logged into Runbook's dashboard click the **Add Reactions** link in the side navigation menu.

![Add Reaction](img/usertuts/http-commando-recipe/runbook-add-reactions.jpg)

Once on the create reactions page simply click the Commando button.

![Select Commando](img/usertuts/http-commando-recipe/runbook-select-commando.jpg)

_This tutorial covers creating a Commando reaction that executes on a single server, by replacing the single server id with a group id these same steps can be followed for groups of servers._

For a single server click the **Create** button under the "Execute Recipe (Single Server) via Commando" reaction.

![Single Server](img/usertuts/http-commando-recipe/runbook-select-execution-type.jpg)

At this point you should be on the creation page for the Commando reaction. If you already know the details required for the reaction you can fill out the form and click **Submit**. You can then skip to the next section of this tutorial. If you do no not have all of the details than follow the steps below.

### Creating the Reaction

![Create Reaction](img/usertuts/http-commando-recipe/runbook-create-reaction.jpg)

The below details are a walk-through of what to put into the Commando reaction form. The values are generic and can be changed to meet your requirements.

#### Name

The name field is generic field that allows you to put a custom name to this reaction.

#### Trigger

The trigger field allows you to define the number of instances a monitor must return the desired result before executing the reaction. To put it simply our HTTP monitor will need to return `False` the number of times defined in this field before Runbook will tell Commando to execute the recipe.

For this tutorial we will set the trigger value to `2`.

#### Frequency

The frequency field allows you to define how often (in seconds) a reaction can be called. In this example we are using `600` which means this reaction will be executed every 10 minutes until the monitor returns to the desired state.

#### Call On

The call on field allows you to define what state the monitor must return for this reaction to be executed. For our example we will want the reaction to execute during `False` states, when our web-server is returning HTTP status codes other than `200 OK`.

#### Quick Note about the above details

From the above settings our reaction should only be called after the monitor has returned 2 `False` states. Once called and executed successfully, the reaction will only be rerun every 10 minutes until the monitor status returns to a `True` state. This is due to our above settings, an important item is if the frequency was set to 0 than our reaction would execute every time a monitor returned a `False` state until the reaction returned a `True` state and reset the trigger counters internal to Runbook.

#### API Key

The API Key field is a simple field that should contain your Commando API Key. If you have not generated an API Key yet, you can follow the instructions on [Commando's API Walk-through video](http://vimeo.com/107547330).

#### Account Alias

The account alias field should contain your account alias (commonly your company name) from Commando. If you are unfamiliar with this value you can find it in the URL of the dashboard, the Commando format is `https://<accountalias>.commando.io`.

#### Server ID

The server id field should contain the unique ID value of the server you want to execute the recipe on. To obtain this value on the Commando Dashboard navigate to the **"Servers"** page and click the server in question.

![Select Server](img/usertuts/http-commando-recipe/select-server.jpg)

Once the server is selected you should see a pop-up with the servers details, scroll down until you see the server id.

![Server ID](img/usertuts/http-commando-recipe/select-server-id.jpg)

#### Recipe ID

The recipe id field should contain the unique ID value of the recipe you want to execute. To obtain this value on the Commando Dashboard navigate to the **"Recipes"** page and click on the recipe in question.

![Select Recipe](img/usertuts/http-commando-recipe/select-recipe.jpg)

Once on the recipe page you can find the recipe ID in the upper right hand corner.

![Select Recipe](img/usertuts/http-commando-recipe/select-recipe-id.jpg)

#### Halt on Error

The halt on error fields value is sent to Commando, if the recipe called returns with an error this value will tell Commando whether or not to stop executing the recipe on other servers. For this tutorial we will leave this field at the default of `False`.

Once the reaction creation form has been completed click the **Submit** button to create the form. On successful creation you should see a Green notification box at the top of the Runbook Dashboard.

## Creating an HTTP GET Monitor on Runbook 

At this point you will no longer need to be logged into the Commando Dashboard and all items referenced will be from the Runbook Dashboard. This section will cover setting up a monitor that requests a URL and looks for specified response codes.

### How the HTTP GET Monitor works

This monitor will perform an HTTP request using the GET method. When the receiving web-server responds it will provide a status code, that status code is checked against a list of user defined expected status codes. If the returned status code is within the list of expected status codes the monitor will go into a `True` state. Any reactions that are defined as `True` reactions are then executed and reactions defined as `False` are skipped. 

If the status code is not within the expected status codes list the monitor will go into a `False` state.

### Monitor Creation

To begin the monitor creation process we must first navigate to the creation form. In the side navigation menu click the **Add Monitors** link.

![Add Monitors](img/usertuts/http-commando-recipe/runbook-add-monitors.jpg)

Once on the monitor creation page click the **Web Applications** button.

![Select Web Applications](img/usertuts/http-commando-recipe/runbook-select-webapp.jpg)

After selecting the Web Applications monitors a pop-up should show with several specific monitor options. Click the **Create** button for the HTTP/S GET monitor.

![Select Web Applications](img/usertuts/http-commando-recipe/runbook-select-get.jpg)

At this point you should be on the monitor creation page. The following will walk you through filling out the HTTP GET monitor creation form. If you are already familiar with this process feel free to skip ahead to the next section.

![Creating Monitor](img/usertuts/http-commando-recipe/runbook-create-monitor.jpg)

#### Name

The name field is a user defined name that can be used to search and find this monitor from the Runbook Dashboard.

#### Reactions

The reactions multi-select box allows you to attach one or many reactions to the monitor being created. For this tutorial simply select the reaction created in the previous step.

![Select Reaction](img/usertuts/http-commando-recipe/runbook-select-reaction.jpg)

#### Time Interval

The time interval field allows you to select the frequency of the monitor. Pro accounts will see more options than the default `30` and `5` minute intervals. For this example we will select the `5` minute interval.

#### Monitoring Zone

The monitoring zone field allows you to define which monitoring servers/regions the monitor should run from. You can currently select up to 2 zones per monitor.

#### URL

The URL field should contain the URL to request. If you want to monitor a specific server and the domain name has multiple IP's you can simply replace the domain with the IP in this field.

For example, if you want to monitor the server at `10.0.0.1` for the `http://example.com/status` URL simply input `http://10.0.0.1/status`.

#### Domain to request

The domain to request field will be used to populate the `host` header. This value should contain the domain to be requested. Using our previous example the domain would be `example.com`.

#### Expected response codes

The expected response codes is a multi-select field that allows you to select the status codes that are expected. For our example we will select the `200` status code.

![Select Status Codes](img/usertuts/http-commando-recipe/runbook-select-statuscodes.jpg)

Once you have selected all of the status codes that are expected simply click the **Submit** button.

## Testing the recipe

At this point our Runbook recipe is created and monitoring our web-server. In order to test the monitor and reaction we can simply manually set the monitor as `False`. To test the monitor we must first be on the **Status** page which is the default page when you login.

From the status page click the **Manage Monitors/Reactions** tab.


![Manage Mons](img/usertuts/http-commando-recipe/runbook-manage.jpg)

Once on the Manage tab simply find the monitor created as part of this tutorial and click the **Mark False** button.

![Test False](img/usertuts/http-commando-recipe/runbook-test-failed.jpg)

After a few minutes you should receive an email from Commando stating that the execution was successful.

![Commando Email](img/usertuts/http-commando-recipe/commando-email.jpg)

To reset the monitor simply click the **Mark True* button on the Manage tab.

## Summary

At this point we have a working HTTP GET monitor that will monitor our web application for `200 OK` response codes. If the monitor detects that the web application is not replying with a `200 OK` for 10 minutes it will execute a reaction that makes an API request to Commando and execute a recipe that simply restarts nginx. This recipe will repeat every 10 minutes until the web application replies with a `200 OK` status code.

## Runbook Community Tutorials

This tutorial is part of Runbook's [community tutorials](index.md). This tutorial was written as part of Runbook's tutorial bounty, where users of Runbook can write tutorials and receive a percentage of ownership in Runbook for their contribution. To find out more go to our [bounty description](https://assembly.com/runbook/bounties/141).
