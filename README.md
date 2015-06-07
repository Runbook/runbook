Runbook
===========

| Facility | Develop | Master |
| --------- | --------| ------------ |
| Travis-CI | [![Build Status](https://travis-ci.org/asm-products/cloudroutes-service.svg?branch=develop)](https://travis-ci.org/asm-products/cloudroutes-service) | [![Build Status](https://travis-ci.org/asm-products/cloudroutes-service.svg?branch=master)](https://travis-ci.org/asm-products/cloudroutes-service)
| Coverage | [![Coverage Status](https://img.shields.io/coveralls/asm-products/cloudroutes-service.svg)](https://coveralls.io/r/asm-products/cloudroutes-service?branch=develop) | N/A |
| Contribute | <a href="https://assembly.com/runbook/bounties?utm_campaign=assemblage&utm_source=runbook&utm_medium=repo_badge"><img src="https://asm-badger.herokuapp.com/runbook/badges/tasks.svg" height="20px" alt="Open Bounties" /> | N/A |

## What is Runbook

[Runbook](https://runbook.io) is an open source monitoring service that allows you to perform automated "reactions" when issues are detected. Giving you the ability to automatically resolve DevOps alerts with zero human interaction.

Simply put, Runbook is what you would get if Nagios and IFTTT had a baby.

## Documentation

Developer and User docs can be found in the [docs](docs/) directory and on [ReadTheDocs](https://runbook.readthedocs.org).

## Open Source

Runbook is 100% open source and developed using the [Assembly](https://assembly.com/runbook) platform. Runbook runs as a SaaS application, there are both free and paid plans; with the Assembly platform all revenue from the product is funnelled into the project and it's contributors. Essentially, after subtracting the cost of business, 10% goes to Assembly as a fee and the rest is given back to the contributors based on a percentage of their contributions.

Unlike other open source products, not only do you get the satisfaction of giving back to the community as a whole but you also get a cut of the profits. To get started simply join us on our [Assembly Project Page](https://assembly.com/runbook)

## Contributing

At Runbook we follow the [GitHub Flow](https://guides.github.com/introduction/flow/index.html), while it is not necessarily manditory that you create feature branches it does help keep code organized. Below are the basic getting started steps for setting up a repo to contribute.

### Setting up your Repo

The first step in getting ready to contribute is forking our repository on github. Once it is forked you can clone that fork onto your desktop; this documentation is assuming you are working from a clone of your fork.

#### Cloning

To pull the repository to your local machine simply run the following.

    $ git clone <url of your repo>


### Setting up your development environment

`devhelpers/` provides you with helper tools to ease your development effort.

It is advisable to get a custom Python `virtualenv` setup for your runbook development.

To install the `devhelpers/` tools, run the following


    $ cd devhelper
    $ make dev-env

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

    $ git remote add upstream git@github.com:asm-products/cloudroutes-service.git

##### Fetching and Merging updates

Once the upstream repository is set you can update your repo by fetching and merging the updates.

    $ git checkout develop
    $ git fetch upstream
    $ git merge upstream/develop
    $ git checkout master
    $ git merge upstream/master

To keep your GitHub fork up to date you can push the changes to your `origin` repository

    $ git push origin
