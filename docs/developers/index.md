## What is Runbook?

[Runbook](https://runbook.io) is an open source monitoring service that allows you to perform automated "Reactions" when issues are detected. Runbook gives you the ability to automatically resolve DevOps alerts with zero human interaction.

Simply put, Runbook is what you would get if Nagios and IFTTT had a baby.

## Open source

Runbook is 100% open source and developed using the [Assembly](https://assembly.com/runbook) platform. Runbook runs as a SaaS application, with both free and paid plans.

With the Assembly platform, all revenue from the product is funneled into the project and its contributors. After subtracting business expenses, 10% goes to Assembly as a fee and the rest is given back to project contributors based on a percentage of their contributions.

Unlike other open source products, not only do you get the satisfaction of giving back to the community as a whole but you also get a cut of the profits. To get started, simply join us on our [Assembly Project Page](https://assembly.com/runbook).

## Contributing

At Runbook, we follow the [GitHub Flow](https://guides.github.com/introduction/flow/index.html). While it is not necessarily mandatory that you create feature branches to contribute to Runbook, it does help keep code organized. Below are the basic steps for setting up a repo to contribute.

### Setting up your repo

The first step in getting ready to contribute is forking [our repository](https://github.com/asm-products/cloudroutes-service) on GitHub. Once it is forked, you can clone that fork onto your desktop. This documentation assumes you are working from a clone of your fork.

#### Cloning

To pull the repository to your local machine, simply run the following.

    $ git clone <url of your repo>

#### Creating a feature branch

We have two branches `develop` and `master`. All new code must be submitted to the `develop` branch. This branch is considered our testing branch. Once all of the features in the `develop` branch are ready for production, they will be merged to the `master` branch.

To start developing a new feature, simply create a unique branch for that feature.

    $ git checkout develop
    $ git checkout -b new-feature

You can make your changes, commit them and—when complete—push them to your GitHub repo.

    $ git push origin new-feature

#### Creating a pull request

When your code is ready and on GitHub you can create a pull request via the GitHub UI. Once your pull request is created, it is typically best practice to go to the bounty on Assembly and submit your work with a link to the pull request. If the feature you created does not have a bounty created yet, simply create one explaining what you've done and why.

After the bounty or work is submitted it is best to add a comment to the pull request with a link to the bounty. This keeps the code review and merging process quick and easy.

#### Syncing your fork

Runbook is a very fast-paced application. We are making major code changes frequently and it is important that you keep your fork in sync to avoid conflicts. Pull requests with conflicts will not be merged until those conflicts are removed. To keep your repository in sync you can follow these steps.

##### Setting the upstream repository

To synchronize with the upstream repository you must first define it as an upstream source.

    $ git remote add upstream git@github.com:asm-products/cloudroutes-service.git

##### Fetching and merging updates

Once the upstream repository is set, you can update your repo by fetching and merging the updates.

    $ git checkout develop
    $ git fetch upstream
    $ git merge upstream/develop
    $ git checkout master
    $ git merge upstream/master

To keep your GitHub fork up to date you can push the changes to your `origin` repository

    $ git push origin

### Tests

Test-driven development is the ideal development process, and we are working toward that. Right now we are mostly dealing with technical debt, adding tests to cover the current code base. That said, when you add code, make sure you add a test. Every push *should* increase code coverage.

#### Run Tests

Without coverage:

```sh
$ python src/web/tests.py
```

With coverage:

```sh
$ python src/web/cov.py
```

Tests currently only cover the web application in "src/web".

---