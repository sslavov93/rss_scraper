# RSS Feed Aggregator
A persistent feed aggregation API

## High Level Overview
This app has two main modules

1. Aggregator
2. User-facing Application

### The Aggregator - `feed/celery_periodic/`
Utilizes Celery Beat's periodic execution capabilities to frequently download feed data, specified under `feeds` in `config.py`.
Every time the task is executed, it calls an instance of a parser (defined in `default_scraper.py`).
It handles the download, parsing and persistence of new feed items.
Each feed item's time of publication is checked and the Feeds's 'LastUpdated' metadata is updated in the Database, according to the most recent published FeedItem.

### The User-Facing Application - `feed/`
A Flask-based API that provides several methods for feed subscriptions and feed posts.
It handles the management of a user's personally subscribed feeds as well as searches of read/unread feed posts.
All operations require a basic form of authentication

## Pre-requisites and External Dependencies
 1. Python 3 - this project assumes [Python 3.7](https://www.python.org/downloads/) is installed
 2. [direnv](https://direnv.net/) - Because it activates the project's virtual environment when you `cd` to the project's folder. There is an included `.envrc` file that should be enough to get you started as long as you run `direnv allow` the first time you enter the cloned repo's root folder.
    * It's fine to use [virtualenv](https://virtualenv.pypa.io/en/latest/), just make sure to copy the environment variables from `.envrc`
 3. [Docker](https://docs.docker.com/get-docker/) - the whole setup runs as a `docker-compose` cluster of containers

    External Container Dependencies (No need to download them in advance):
    * [Postgres](https://hub.docker.com/_/postgres) (Storage)
    * [Rabbitmq](https://hub.docker.com/_/rabbitmq) (Connection between the celery workers and the broker)

## Installation
 1. Clone the repository
 2. Run `pip3 install -r requirements.txt` to download the project's dependencies

### First time setup
 1. In a new terminal window run `docker-compose run queue`
 2. In a new terminal window run `docker-compose run storage`
 3. In a new terminal window run `fab init` - this sets up permissions with the queue and pre-populates the database

## Runing the App
 1. Run `docker-compose up`.
 2. ONLY THE FIRST TIME, run `fab initdb` - this will populate the database with some sample data

For a more visual example of the API, open `http://localhost:1337/swagger` - it's interactive and allows to test requests on the fly

### Testing
With the `postgres` container running,
Simply run `fab test` from the root of the project.

## Deployment
The application is in a state in which newly committed changes can be picked up from a build system (Jenkins, Travis, etc.) and then fresh Docker images can be spun up but this is way beyond the purpose of this exercise

## Developer Comments and TODOs
Additional thoughts of improvement

### TODOs
 * Extend the Flask App with forms and templates, accessible through a browser.

### Comments
 * In a production environment, I would expect a credential service that takes care of the environment to be populated with the proper variables, which this app will utilize.
 * For better partition tolerance and higher maintainability, the Celery workers should be separated from the main App container (+ it makes the logging easier to scan through)
 * There are some commands that are executed on the `rabbitmq` container as part of the `fab init` task. This is a hack - in a production environment I would expect this to be provisioned and maintained elsewhere, so the feed aggregator app only consumes it.
 * No Git branches have been used, to avoid dealing with unnecessary merge conflicts, since I'm the only one maintaining this project (for now). In an actual prod environment this is unacceptable and bears a huge risk.
 
In general, the design of this app is not very robust the more feeds and feed items are present because the Read / Unread searches are a big bottleneck.
In practice, what I will do, is rely on some more elaborate message broker system, which the clients will be responsible for pulling new items from.