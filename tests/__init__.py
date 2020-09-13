import base64
import unittest
from datetime import datetime

import pytz
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from sqlalchemy_utils import database_exists, drop_database, create_database

from config import TestConfig
from feed import create_app, db
from feed.models import User, Feed, Follows, FeedItem, Unread, Read


def basic_auth_headers(username, password):
    creds = base64.b64encode(bytes(f"{username}:{password}", "utf-8")).decode("utf-8")
    return {'Authorization': 'Basic ' + creds}


class BaseTestFixture(unittest.TestCase):
    app = create_app()
    client = app.test_client()
    database = db
    url = TestConfig.SQLALCHEMY_DATABASE_URI


    @classmethod
    def setUpClass(cls):
        if database_exists(cls.url):
            drop_database(cls.url)
        create_database(cls.url)

        with cls.app.app_context():
            db.create_all()

            user1 = User(username="user", password=pbkdf2_sha256.hash("pass"))
            user2 = User(username="user2", password=pbkdf2_sha256.hash("pass"))
            user3 = User(username="user3", password=pbkdf2_sha256.hash("pass"))

            feed_dt = datetime(year=2020, month=9, day=1, hour=0, minute=0, second=0, microsecond=0, tzinfo=pytz.utc)
            item_dt = datetime(year=2020, month=9, day=9, hour=0, minute=0, second=0, microsecond=0, tzinfo=pytz.utc)
            feed1 = Feed(id=1, url="https://feeds.feedburner.com/tweakers/mixed", parser="html5lib",
                         time_format="%a, %d %b %Y %H:%M:%S %Z", last_updated=feed_dt)
            feed2 = Feed(id=2, url="http://www.nu.nl/rss/Algemeen", parser="lxml",
                         time_format="%a, %d %b %Y %H:%M:%S %z",
                         last_updated=feed_dt)

            follows1 = Follows(username=user1.username, feed_id=feed1.id)
            follows2 = Follows(username=user2.username, feed_id=feed2.id)

            item1 = FeedItem(
                id=1, url="https://stackoverflow.com/", title="Item 1", description="Desc 1", feed_id=1,
                published=item_dt)
            item2 = FeedItem(
                id=2, url="https://www.quora.com/", title="Item 2", description="Desc 2", feed_id=1, published=item_dt)
            item3 = FeedItem(
                id=3, url="https://stackoverflow.com/", title="Item 3", description="Desc 3", feed_id=2,
                published=item_dt)
            item4 = FeedItem(
                id=4, url="https://www.quora.com/", title="Item 4", description="Desc 4", feed_id=2, published=item_dt)

            unread1 = Unread(username=user1.username, item_id=1, feed_id=1)
            read1 = Read(username=user1.username, item_id=2, feed_id=1)
            unread2 = Unread(username=user2.username, item_id=3, feed_id=2)
            read2 = Read(username=user2.username, item_id=4, feed_id=2)

            db.session.add_all(
                [user1, user2, user3, feed1, feed2, follows1, follows2, item1, item2, item3, item4, unread1, unread2, read1, read2])
            db.session.commit()

    # @classmethod
    # def tearDownClass(cls):
    #     if database_exists(cls.url):
    #         drop_database(cls.url)
