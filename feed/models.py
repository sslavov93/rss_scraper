from passlib.hash import pbkdf2_sha256
from feed import db


class User(db.Model):
    __tablename__ = "users"

    username = db.Column(db.String(256), primary_key=True)
    password = db.Column(db.String(128))

    def hash_password(self, password):
        self.password = pbkdf2_sha256.hash(password)

    def verify_password(self, password):
        return pbkdf2_sha256.verify(password, self.password)

    def __repr__(self):
        return f"User(username='{self.username}')"


class Feed(db.Model):
    __tablename__ = "feeds"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(2000))
    parser = db.Column(db.String(20))
    time_format = db.Column(db.String(50))
    last_updated = db.Column(db.TIMESTAMP(timezone=True))

    def serialize(self):
        return {
            'id': self.id,
            'url': self.url
        }

    def __repr__(self):
        return f"'id': '{self.id}', 'url': '{self.url}', 'parser': '{self.parser}', 'time_format': '{self.time_format}', 'last_updated': '{self.last_updated}'"


class FeedItem(db.Model):
    __tablename__ = "feed_items"

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(2000))
    title = db.Column(db.String(100))
    description = db.Column(db.String(5000))
    feed_id = db.Column(db.Integer, db.ForeignKey('feeds.id'))
    feed = db.relationship('Feed', backref=db.backref('feed_items', lazy=True))
    published = db.Column(db.TIMESTAMP(timezone=True))

    def serialize(self):
        return {
            'id': self.id,
            'url': self.url,
            'title': self.title,
            'description': self.description,
            'published': self.published,
        }

    def __repr__(self):
        return f"FeedItem(id='{self.id}', title='{self.title}', feed_id='{self.feed_id}', url='{self.url}', published='{self.published}')"


class Follows(db.Model):
    __tablename__ = "follows"

    id = db.Column(db.Integer(), primary_key=True)

    username = db.Column(db.String, db.ForeignKey('users.username'))
    user = db.relationship('User', backref=db.backref('follows', lazy=True))

    feed_id = db.Column(db.Integer, db.ForeignKey('feeds.id'))
    feed = db.relationship('Feed', backref=db.backref('follows', lazy=True))

    def __repr__(self):
        pass


class Unread(db.Model):
    __tablename__ = "unreads"

    id = db.Column(db.Integer(), primary_key=True)

    username = db.Column(db.String, db.ForeignKey('users.username'))
    user = db.relationship('User', backref=db.backref('unreads', lazy=True))

    item_id = db.Column(db.Integer, db.ForeignKey('feed_items.id'))
    item = db.relationship('FeedItem', backref=db.backref('unreads', lazy=True))

    feed_id = db.Column(db.Integer, db.ForeignKey('feeds.id'))
    feed = db.relationship('Feed', backref=db.backref('unreads', lazy=True))


class Read(db.Model):
    __tablename__ = "reads"

    id = db.Column(db.Integer(), primary_key=True)

    username = db.Column(db.String, db.ForeignKey('users.username'))
    user = db.relationship('User', backref=db.backref('reads', lazy=True))

    item_id = db.Column(db.Integer, db.ForeignKey('feed_items.id'))
    item = db.relationship('FeedItem', backref=db.backref('reads', lazy=True))

    feed_id = db.Column(db.Integer, db.ForeignKey('feeds.id'))
    feed = db.relationship('Feed', backref=db.backref('reads', lazy=True))
