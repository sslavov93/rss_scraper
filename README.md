# RSS Feed Aggregator

## High Level Overview
This app has two main modules

1. Aggregator
2. User-facing Application

### The Aggregator - `feed/celery_periodic/`
Utilizes Celery Beat's periodic execution capabilities to frequently download feed data, specified under `feeds` in `config.py`.
Every time the task is executed, it calls an instance of a parser (defined in `default_scraper.py`).
It handles the download, parsing and persistence of new feed items.
Each feed item's time of publication is checked and the Feeds's `Last Updated` metadata is updated in the Database, according to the most recent published FeedItem.

### The User-Facing Application - `feed/`
A Flask-based API that provides the user several methods to manage feed item subscriptions and read/unread feed items.
It handles delivery of feed items 

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


## Runing the app setup
 1. Run `docker-compose up`.
 2. ONLY THE FIRST TIME, run `fab initdb` - this will populate the database with some sample data

For a more visual example of the API, access `localhost:5000/swagger` - it's interactive and allows to test requests on the fly

### Testing

Simply run `fab test` from the root of the project.

## Deployment
Run `fab deploy` - note that this depends on you having proper Docker Hub credentials or other means of authenticating with a private Docker repository

## Dev Commentary and TODOs
Additional thoughts if improvement
### TODOs
 * Extend the Flask App with forms and templates, accessible through a browser.

### Commentary
 * For better pertition tolerance and higher maintainability, the Celery workers should be separated from the main App container
 