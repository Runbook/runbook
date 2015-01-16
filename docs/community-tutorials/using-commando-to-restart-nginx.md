# Using Runbook and Commando to monitor and automatically restart nginx

## Introduction

In this tutorial you will learn how to setup a Runbook recipe that will ensure the nginx service is always responding with a `200 OK` response code.

At the end of this tutorial you will have a recipe setup that performs the following tasks.

1. Monitor nginx with an HTTP GET request
2. If the request fails or does not reply with `200 OK` restart nginx by executing a predefined Commando recipe

## Pre-requisites

This tutorial assumes the following:

* You already have at minimum a free account on [Runbook](https://dash.runbook.io/signup)
* You already have an account with [Commnado](https://commando.io) that has API accesss (required for Runbook integration)
* You have already defined and connected the servers in question on Commando
  * If this step is not already complete you can follow this [walkthrough from Commando](http://vimeo.com/73097569)


