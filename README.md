# RSS Feed Aggregator
A persistent feed aggregation API

## High Level Overview
This app has two main modules:
1. Aggregator
2. User-facing Application

### The Aggregator - `rss_scraper/feed/celery_periodic/`
Utilizes Celery Beat's periodic execution capabilities to frequently download feed data, specified under `feeds` in `config.py`.
Every time the task is executed, it calls an instance of a parser (defined in `default_scraper.py`).
It handles the download, parsing and persistence of new feed items.
Each feed item's time of publication is checked and the Feeds's 'LastUpdated' metadata is updated in the Database, according to the most recent published FeedItem.

### The User-Facing Application - `rss_scraper/feed/`
A Flask-based API that provides several methods for feed subscriptions and feed posts.
It handles the management of a user's personally subscribed feeds as well as searches of read/unread feed posts.
All operations require a basic form of authentication

## Deep Dive
This app models Users, Feeds and FeedItems, as well as some relationships between them.
`Users` can register, follow and unfollow `Feeds`, read new unread `FeedItems` and examine already read `FeedItems`.
`Follows` shows which user follows which feed.
`Read` and `Unread` show which feed item was read / unread from which user.
All can be examined in more technical detail in `rss_feed/feed/models.py`

Starting point - `config.Config.feeds` - this is where new feeds are declared - the program needs a valid feed URL, a Markup Parser to be used by the HTML parser library to extract necessary data and formatting of the date and time the feed post was published.
Initial two feeds, that were provided were [Tweakers](https://feeds.feedburner.com/tweakers/mixed) and [Algemeen](http://www.nu.nl/rss/Algemeen). Their similarity lead to just one scraper class (`rss_scraper/feed/celery_periodic/scraper.py`) but in the event that other feeds with different characteristics are added, this class can be used as a base parent class and the difference in characteristics be overridden in a child class.

Whenever the app detects newer posts (comparing with the last time a check was done, default for prod is 10 minutes), it writes them in a database.
For each item it also creates unread relationships for each of the user that is following the feed that item was scraped from.

Users can then request new unread feed_items, based on the feeds they follow and choose which item (or a collection of items) to mark* as read.
  * mark as read - remove the `Unread` relationship between a specific item and a specific user and create a `Read` relationship. This is helpful for search queries based on whether the user wants new unread items or read items

For a more visual example of the different operations the API provides, open `http://localhost:1337/swagger` - it's interactive and allows to test requests on the fly.


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

## Runing the App
 1. Run `docker-compose up`.
 2. **Important** The first time you start the app, run `fab initdb`
    1. This will pre-populate the database with feeds to crawl from


## Environment and configuration
 * For this example, the production and development environment are the same, in a life scenario this will be, of course, separated
 * Configuration is loaded from `config.py`, everything for the Testing and Development config is hardcoded.
   * For the purposes of this exercise, the "production" values are copied in the docker images from a file called `docker/prod.env`
    
### Local Development Server
With the containers running, in a separate terminal window run `fab serve` from the root of the project.

### Testing
With the containers running, in a separate terminal window run `fab test` from the root of the project.

### Deployment
The application should be in a state in which newly committed changes can be picked up from a build system (Jenkins, Travis, etc.) and then fresh Docker images can be spun up from the provided `docker-compose.yml` but this is way beyond the purpose of this exercise.

## Developer Comments and TODOs
Additional thoughts of improvement

### TODOs
 * Extend the Flask App with forms and templates, accessible through a browser.
 * At the moment, the config objects (found in `config.py`) rely on Env Variables and build connection URLs from that. The file looks ugly, a better approach might be experimenting with yaml files and inheritance for different envs.
    
### Comments
 * In a production environment, I would expect a credential service that takes care of the environment to be populated with the proper variables, which this app will utilize.
 * For better partition tolerance and higher maintainability, the Celery workers should be separated from the main App container (+ it makes the logging easier to scan through)
 * There are some commands that are executed on the `rabbitmq` container as part of the `fab init` task. This is a hack - in a production environment I would expect this to be provisioned and maintained elsewhere, so the feed aggregator app only consumes it.
 * No Git branches have been used, to avoid dealing with unnecessary merge conflicts, since I'm the only one maintaining this project (for now). In an actual prod environment this is unacceptable and bears a huge risk.
 
In general, the design of this app is not very robust the more feeds and feed items are present because the Read / Unread searches are a big bottleneck.
In practice, what I will do, is rely on some more elaborate message broker system, which the clients will be responsible for pulling new items from.