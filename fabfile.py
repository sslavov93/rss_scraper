import os

from fabric import task
from invoke import run

from feed import create_app
from sqlalchemy_utils import database_exists, create_database, drop_database


@task
def test(context, env='testing'):
    os.environ['FLASK_ENV'] = env
    run("coverage run --source=tests/ -m pytest ")


@task
def docs(context):
    pass


@task
def serve(context):
    run("flask run")


@task
def init(context, env="development"):
    init_rabbitmq()
    init_db()


@task
def init_rabbitmq(context, env="development"):
    run("docker exec -it rabbitmq rabbitmqctl add_user user password 2>/dev/null ")
    run("docker exec -it rabbitmq rabbitmqctl set_user_tags user administrator")
    run("docker exec -it rabbitmq rabbitmqctl set_permissions -p / user  \".*\" \".*\" \".*\"")


@task
def init_db(context, env='development'):
    os.environ['FLASK_ENV'] = env

    url = "postgresql://postgres:dbpw@localhost:5432/feedaggregator"
    url += "" if env != 'testing' else "_test"

    if database_exists(url):
        print("dropping")
        drop_database(url)
    print("creating")
    create_database(url)

    app = create_app()
    # with app.app_context():
    #     db.create_all()
    #
    #     user1 = User(username="user", password=pbkdf2_sha256.hash("pass"))
    #     user2 = User(username="user2", password=pbkdf2_sha256.hash("pass"))
    #
    #     feed_dt = datetime(year=2020, month=9, day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=pytz.utc)
    #     item_dt = datetime(year=2020, month=9, day=9, hour=0, minute=0, second=0, microsecond=0, tzinfo=pytz.utc)
    #     feed1 = Feed(id=1, url="https://feeds.feedburner.com/tweakers/mixed", parser="html5lib",
    #                  time_format="%a, %d %b %Y %H:%M:%S %Z", last_updated=feed_dt)
    #     feed2 = Feed(id=2, url="http://www.nu.nl/rss/Algemeen", parser="lxml",
    #                  time_format="%a, %d %b %Y %H:%M:%S %z",
    #                  last_updated=feed_dt)
    #
    #     follows1 = Follows(username=user1.username, feed_id=feed1.id)
    #     follows2 = Follows(username=user2.username, feed_id=feed2.id)
    #
    #     item1 = FeedItem(
    #         id=1, url="https://stackoverflow.com/", title="Item 1", description="Desc 1", feed_id=1,
    #         published=item_dt)
    #     item2 = FeedItem(
    #         id=2, url="https://www.quora.com/", title="Item 2", description="Desc 2", feed_id=1, published=item_dt)
    #     item3 = FeedItem(
    #         id=3, url="https://stackoverflow.com/", title="Item 3", description="Desc 3", feed_id=2,
    #         published=item_dt)
    #     item4 = FeedItem(
    #         id=4, url="https://www.quora.com/", title="Item 4", description="Desc 4", feed_id=2, published=item_dt)
    #
    #     unread1 = Unread(username=user1.username, unread_item=1, feed_id=1)
    #     unread2 = Unread(username=user1.username, unread_item=2, feed_id=1)
    #     unread3 = Unread(username=user2.username, unread_item=3, feed_id=2)
    #     unread4 = Unread(username=user2.username, unread_item=4, feed_id=2)
    #
    #     db.session.add_all([user1, user2, feed1, feed2, follows1, follows2, item1, item2, item3, item4, unread1, unread2, unread3, unread4])
    #     db.session.commit()
    #     print("DONE.")


@task
def migratedb(context):
    run("python3 manage.py db migrate")
    run("python3 manage.py db upgrade")
