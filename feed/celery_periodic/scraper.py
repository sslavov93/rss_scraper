import pytz
import requests
from bs4 import BeautifulSoup
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import MultipleResultsFound

from feed.models import FeedItem, Feed, Follows, Unread
from feed import db
from datetime import datetime
import logging


class Scraper:
    """A class that scans provided feed urls for new posts and persists them in a database

    The implementation downloads the full content of the feed page, parses it according to specific feed details
    in config.py (project root) and extracts the new posted feed items. They are then persisted in the database and
    specific relationship details are created for each user that follows the specified feed.
    """
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    def __init__(self, feed):
        url = feed.get("url")
        feeds = Feed.query.filter_by(url=url).all()

        # Multiple entries found in the database for a given url - this indicates an error
        if len(feeds) > 1:
            msg = "More than one entry for feed URL found. Aborting."
            self.logger.error(msg, MultipleResultsFound)
            raise MultipleResultsFound(msg)
        # we don't have an entry in the database yet
        elif len(feeds) < 1:
            now = datetime.utcnow()
            dt = datetime(year=now.year, month=now.month, day=now.day,
                          hour=now.hour, minute=now.minute, second=now.second, tzinfo=pytz.utc)

            f = Feed(url=url, parser=feed.get("parser"), time_format=feed.get("time_format"), last_updated=dt)
            db.session.add(f)
            db.session.commit()

        self.feed = feeds[0]

    @staticmethod
    def get_title(feed_item):
        """Gets the title of a single parsed feed item in the form of a string"""
        return feed_item.title.string

    @staticmethod
    def get_description(feed_item):
        """Gets the description of a single parsed feed item in the form of a string"""
        return feed_item.description.string

    @staticmethod
    def get_url(feed_item):
        """Gets the URL of a single parsed feed item in the form of a string"""
        return feed_item.link.next

    def get_published_time(self, feed_item):
        """Calculates the time of publication of a single parsed feed item in the form of a datetime object"""
        date = datetime.strptime(feed_item.pubdate.string, self.feed.time_format)
        time_of_publication = datetime(
            year=date.year, month=date.month, day=date.day, hour=date.hour,
            minute=date.minute, second=date.second, tzinfo=pytz.utc if not date.tzinfo else date.tzinfo
        )

        return time_of_publication

    def build_db_object(self, unparsed_feed_item):
        """Prepares a FeedItem object ready for persistence in the database"""
        return FeedItem(
            url=self.get_url(unparsed_feed_item),
            title=self.get_title(unparsed_feed_item),
            description=self.get_description(unparsed_feed_item),
            feed_id=self.feed.id,
            published=self.get_published_time(unparsed_feed_item)
        )

    def parse(self):
        """Downloads the content of the specified feed url and prepares persistence-ready database FeedItem objects"""
        try:
            response = requests.get(self.feed.url)
            if response.content:
                soup = BeautifulSoup(response.content, self.feed.parser)
                items = []

                for feed_item in soup.find_all("item"):
                    if self.feed.last_updated < self.get_published_time(feed_item):
                        db_feed_item = self.build_db_object(feed_item)
                        items.append(db_feed_item)
                return items
            return []
        except ConnectionError as err:
            self.logger.error(f"Connection for url '{self.feed.url}' not available. Aborting.", err)
            raise err
        except (AttributeError, KeyError) as err:
            self.logger.error(f"Problem parsing data for feed '{self.feed.url}'", err)
            raise err
        except Exception as err:
            raise err

    def persist(self, feed_items):
        """Persists a list of FeedItem objects in the database

        :param feed_items: The collection of FeedItem objects to be persisted
        :type feed_items: list
        """
        try:
            if feed_items:
                db.session.add_all(feed_items)

                # Add an Unread relationship between each new item and each user that follows current feed
                users_that_follow_current_feed = Follows.query.filter_by(feed_id=self.feed.id).all()
                for item in feed_items:
                    if users_that_follow_current_feed:
                        for user in users_that_follow_current_feed:
                            unread = Unread(username=user.username, item_id=item.id)
                            db.session.add(unread)

                # Update the last_updated timestamp of the specific Feed
                date = datetime.now()
                last_updated = datetime(year=date.year, month=date.month, day=date.day, hour=date.hour,
                                        minute=date.minute, second=date.second,
                                        tzinfo=pytz.utc if not date.tzinfo else date.tzinfo)
                self.feed.last_updated = last_updated
                db.session.add(self.feed)
                db.session.commit()
        except SQLAlchemyError as err:
            db.session.rollback()
            self.logger.error(f"Problem interacting with the database", err)
            raise err
        except Exception as err:
            raise err
