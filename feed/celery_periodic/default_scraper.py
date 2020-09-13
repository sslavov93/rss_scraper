import pytz
import requests
from bs4 import BeautifulSoup
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import MultipleResultsFound

from feed.models import FeedItem, Feed, Follows, Unread
from feed import db
from datetime import datetime
import logging


class DefaultParser:
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)

    def __init__(self, feed_url):
        feeds = Feed.query.filter_by(url=feed_url).all()
        if len(feeds) != 1:
            msg = "More than one entry for feed URL found. Aborting."
            self.logger.error(msg, MultipleResultsFound)
            raise MultipleResultsFound(msg)

        self.feed = feeds[0]

    @staticmethod
    def get_title(feed_item):
        return feed_item.title.string

    @staticmethod
    def get_description(feed_item):
        return feed_item.description.string

    @staticmethod
    def get_url(feed_item):
        return feed_item.link.next

    def get_published_time(self, feed_item):
        date = datetime.strptime(feed_item.pubdate.string, self.feed.time_format)
        time_of_publication = datetime(
            year=date.year, month=date.month, day=date.day, hour=date.hour,
            minute=date.minute, second=date.second, tzinfo=pytz.utc if not date.tzinfo else date.tzinfo
        )

        return time_of_publication

    def build_db_object(self, unparsed_feed_item):
        return FeedItem(
            url=self.get_url(unparsed_feed_item),
            title=self.get_title(unparsed_feed_item),
            description=self.get_description(unparsed_feed_item),
            feed_id=self.feed.id,
            published=self.get_published_time(unparsed_feed_item)
        )

    def parse(self):
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
        except AttributeError as err:
            self.logger.error(f"Problem parsing data for feed '{self.feed.url}'", err)
            raise err
        except KeyError as err:
            self.logger.error(f"Problem parsing data for feed '{self.feed.url}'", err)
            raise err
        except Exception as err:
            raise err

    def persist(self):
        try:
            feed_items = self.parse()

            if feed_items:
                db.session.add_all(feed_items)

                # TODO This needs to be fixed to happen for users in follows table ONLY
                users_that_follow_current_feed = Follows.query.filter_by(feed_id=self.feed.id).all()
                for item in feed_items:
                    if users_that_follow_current_feed:
                        for user in users_that_follow_current_feed:
                            unread = Unread(username=user.username, item_id=item.id)
                            db.session.add(unread)

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
