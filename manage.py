from datetime import datetime

import pytz
from flask_migrate import MigrateCommand
from flask_script import Manager, Command

from config import feeds
from feed import create_app, db
from feed.models import Feed

app = create_app()
manager = Manager(app)


class InitDbCommand(Command):
    """ Initialize the database."""

    def run(self):
        init_db()
        print('Database has been initialized.')


def init_db():
    """ Initialize the database."""
    db.drop_all()
    db.create_all()
    create_feeds(db)


def create_feeds(db):
    counter = 1
    for rss_feed in feeds:
        now = datetime.utcnow()
        dt = datetime(now.year - 1, now.month, now.day, now.hour, now.minute, now.second, tzinfo=pytz.utc)
        db.session.add(
            Feed(id=counter, url=rss_feed.get("url"), parser=rss_feed.get("parser"),
                 time_format=rss_feed.get("time_format"), last_updated=dt))
        counter += 1
    db.session.commit()


manager.add_command('db', MigrateCommand)
manager.add_command('init_db', InitDbCommand)


if __name__ == "__main__":
    manager.run()
