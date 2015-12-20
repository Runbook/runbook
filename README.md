Runbook
===========

## What is Runbook

[Runbook](https://runbook.io) is an OpenSaaS (Apache 2.0) monitoring service that allows you to perform automated "reactions" when issues are detected. Giving you the ability to automatically resolve DevOps alerts with zero human interaction.

Simply put, Runbook is what you would get if Nagios and IFTTT had a baby.

## Documentation

Developer and User docs can be found in the [docs](docs/) directory and on [ReadTheDocs](https://runbook.readthedocs.org).

### 3 Step Deployment

You can easily deploy Runbook within a Docker container with 3 simple steps. This deployment should work for small environments, for larger environments checkout our [Installation Guide](http://runbook.readthedocs.org/en/latest/install/).

* Start a RethinkDB Container

```sh
$ sudo docker run -d --name rethinkdb rethinkdb
```
* Start a Redis Container

```sh
$ sudo docker run -d --name redis redis
```
* Start a Runbook Container (linking to Redis and RethinkDB)

```sh
$ docker run -d --name runbook -p 8000:8000 --link rethinkdb:rethinkdb --link redis:redis runbook/runbook
```

Once launched simply navigate to `http://<serverip>:8000`.


[![Docker Pulls](https://img.shields.io/docker/pulls/runbook/runbook.svg)](https://hub.docker.com/r/runbook/runbook/)

## Build Status

**Develop:**

[![Build Status](https://travis-ci.org/Runbook/runbook.svg?branch=develop)](https://travis-ci.org/Runbook/runbook) [![Coverage Status](https://coveralls.io/repos/Runbook/runbook/badge.svg?branch=develop&service=github)](https://coveralls.io/github/Runbook/runbook?branch=develop)

**Master:**

[![Build Status](https://travis-ci.org/Runbook/runbook.svg?branch=master)](https://travis-ci.org/Runbook/runbook) [![Coverage Status](https://coveralls.io/repos/Runbook/runbook/badge.svg?branch=master&service=github)](https://coveralls.io/github/Runbook/runbook?branch=master)


## Contributing

[![Join the chat at https://gitter.im/Runbook/runbook](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/Runbook/runbook?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) [![Stories in Ready](https://badge.waffle.io/Runbook/runbook.svg?label=ready&title=Ready)](http://waffle.io/Runbook/runbook)

At Runbook we follow the [GitHub Flow](https://guides.github.com/introduction/flow/index.html), while it is not required that you create feature branches it does help keep code organized. Below are the basic getting started steps for setting up a repo to contribute.

### Setting up your Repo

The first step in getting ready to contribute is forking our repository on github. Once it is forked you can clone that fork onto your desktop; this documentation is assuming you are working from a clone of your fork.

#### Cloning

To pull the repository to your local machine simply run the following.

    $ git clone <url of your repo>

#### Creating a feature branch

We have two branches `develop` and `master`, all new code must be submitted to the `develop` branch. This branch is considered our testing branch; once all of the features in the `develop` branch are ready for production they will be merged to the `master` branch.

To start developing a new feature simply create a unique branch for that feature.

    $ git checkout develop
    $ git checkout -b new-feature

You can make your changes, commit them and when complete push them to your GitHub repo.

    $ git push origin new-feature

#### Creating a pull request

Once your code is ready and on GitHub you can create a Pull Request via the GitHub UI. Once your pull request is created it is typically best practice to go to the bounty on Assembly and submit your work with a link to the pull request. If the feature you created does not have a bounty created yet, simply create one explaining what you've done and why.

Once the bounty or work is submitted it is best to add a comment to the pull request with a link to the bounty. This keeps the code review and merging process quick and easy.

#### Syncing your fork

Runbook is a very fast paced application, we are making major code changes frequently and it is important that you keep your fork in sync to avoid conflicts. PR's with conflicts will not be merged until those conflicts are removed. To keep your repository in sync you can follow these steps.

##### Setting the upstream repository

To synchronize with the upstream repository you must first define it as an upstream source.

    $ git remote add upstream https://github.com/Runbook/runbook.git

##### Fetching and Merging updates

Once the upstream repository is set you can update your repo by fetching and merging the updates.

    $ git checkout develop
    $ git fetch upstream
    $ git merge upstream/develop
    $ git checkout master
    $ git merge upstream/master

To keep your GitHub fork up to date you can push the changes to your `origin` repository

    $ git push origin
