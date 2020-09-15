import json

from werkzeug.exceptions import HTTPException

from feed import db
from feed.celery_periodic.scraper import Scraper
from feed.models import Feed, User, Follows, FeedItem, Unread, Read
from flask import request, g
from feed import auth
from feed.errors.exceptions import *
from feed.celery_periodic.tasks import scrape_single


@app.route('/api/users', methods=['POST'])
def register():
    if request.json is None:
        log_and_raise(app.logger, MissingRequiredParameter("Missing Request Body", 400, payload=request.json))

    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        log_and_raise(app.logger, MissingRequiredParameter("Username and Password are required", 400, payload=request.json))

    if User.query.filter_by(username=username).first() is not None:
        log_and_raise(app.logger, UserExists("User already exists", status_code=400, payload=request.json))

    user = User(username=username)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()

    app.logger.info(f"User '{username}' registered")
    return jsonify(username=user.username), 201


@app.route("/api/feeds", methods=["GET"])
@auth.login_required
def get_all_feeds():
    feeds = Feed.query.all()
    return jsonify([feed.serialize() for feed in feeds]), 200


@app.route("/api/my-feeds")
@auth.login_required
def get_all_user_subscribed_feeds():
    follows = Follows.query.filter_by(username=g.user.username).all()
    feeds = Feed.query.filter(Feed.id.in_([relationship.feed_id for relationship in follows])).all()
    return jsonify([feed.serialize() for feed in feeds]), 200


@app.route("/api/feeds/follow", methods=["POST"])
@auth.login_required
def follow_feed():
    if request.json is None:
        log_and_raise(app.logger, MissingRequiredParameter("Missing request body", 400, payload=request.json))

    feed_id = request.json.get('feed_id')
    if not feed_id:
        log_and_raise(app.logger, MissingRequiredParameter("Missing 'feed_id' in request body", 400, payload=request.json))

    feed = Feed.query.get(feed_id)
    if not feed:
        log_and_raise(app.logger, FeedNotFound("Feed id not found", 404, payload=request.json))

    follow_relationship = Follows.query.filter_by(username=g.user.username, feed_id=feed_id).first()
    if not follow_relationship:
        db.session.add(Follows(username=g.user.username, feed_id=feed_id))
    else:
        log_and_raise(app.logger, FeedAlreadyFollowed(f"User '{g.user.username}' already follows feed '{feed_id}'", status_code=409))

    feed_items_by_feed_id = FeedItem.query.filter_by(feed_id=feed_id).all()

    for item in feed_items_by_feed_id:
        db.session.add(Unread(username=g.user.username, item_id=item.id, feed_id=feed_id))
    db.session.commit()

    app.logger.info(f"User '{g.user.username}' already follows feed '{feed_id}'")
    return jsonify(""), 204


@app.route("/api/feeds/unfollow", methods=["DELETE"])
@auth.login_required
def unfollow_feed():
    if request.json is None:
        log_and_raise(app.logger, MissingRequiredParameter("Missing request body", 400, payload=request.json))

    feed_id = request.json.get('feed_id')
    if not feed_id:
        log_and_raise(app.logger, MissingRequiredParameter("Missing 'feed_id' in request body", 400, payload=request.json))

    feed = Feed.query.get(feed_id)
    if not feed:
        log_and_raise(app.logger, FeedNotFound("Feed id not found", 404, payload=request.json))

    follow_relationship = Follows.query.filter_by(username=g.user.username, feed_id=feed_id).first()
    if follow_relationship:
        db.session.delete(follow_relationship)
    else:
        raise FeedNotFollowed(f"User '{g.user.username}' does not follow feed '{feed_id}'", status_code=409)

    unnecessary_items = Unread.query.filter_by(username=g.user.username, feed_id=feed_id).all()
    if unnecessary_items:
        for item in unnecessary_items:
            db.session.delete(item)
    db.session.commit()

    app.logger.info(f"User '{g.user.username}' stopped following feed '{feed_id}'")
    return jsonify(""), 204


@app.route("/api/my-feeds/<feed_id>/new")
@auth.login_required
def get_unread_items_from_feed(feed_id):
    feed = Feed.query.get(feed_id)
    if not feed:
        log_and_raise(app.logger, FeedNotFound("Feed id not found", 404, payload=request.json))

    follow_relationship = Follows.query.filter_by(username=g.user.username, feed_id=feed_id).first()
    if not follow_relationship:
        log_and_raise(app.logger, FeedNotFollowed(f"User {g.user.username} does not follow feed {feed_id}", status_code=409))

    unreads = Unread.query.filter_by(username=g.user.username, feed_id=feed_id).all()
    unread_item_ids = [unread.item_id for unread in unreads]
    unread_items = FeedItem.query.filter(FeedItem.id.in_(unread_item_ids)).order_by(FeedItem.published.desc()).all()
    if not unread_items:
        return jsonify({'message': f"No new items from feed '{feed_id}'"}), 200
    return jsonify([item.serialize() for item in unread_items]), 200


@app.route("/api/my-feeds/new")
@auth.login_required
def get_unread_items_from_all_feeds():
    follow_relationships = Follows.query.filter_by(username=g.user.username).all()
    if not follow_relationships:
        return jsonify(f"User '{g.user.username}' does not follow any feeds")

    unread_item_ids = []
    for relationship in follow_relationships:
        unread_items = Unread.query.filter_by(username=g.user.username, feed_id=relationship.feed_id).all()
        if unread_items:
            for unread_item in unread_items:
                unread_item_ids.append(unread_item.item_id)

    unread_items = FeedItem.query.filter(FeedItem.id.in_(unread_item_ids)).order_by(FeedItem.published.desc()).all()
    return jsonify([item.serialize() for item in unread_items]), 200


@app.route("/api/my-feeds/<feed_id>/old")
@auth.login_required
def get_read_items_from_feed(feed_id):
    feed = Feed.query.get(feed_id)
    if not feed:
        log_and_raise(app.logger, FeedNotFound("Feed id not found", 404, payload=request.json))

    follow_relationship = Follows.query.filter_by(username=g.user.username, feed_id=feed_id).first()
    if not follow_relationship:
        log_and_raise(app.logger, FeedNotFollowed(f"User '{g.user.username}' does not follow feed '{feed_id}'", status_code=409))

    reads = Read.query.filter_by(username=g.user.username, feed_id=feed_id).all()
    read_item_ids = [read.item_id for read in reads]
    read_items = FeedItem.query.filter(FeedItem.id.in_(read_item_ids)).order_by(FeedItem.published.desc()).all()
    if not read_items:
        return jsonify({"message": f"Nothing in feed '{feed_id}' has been read."}), 200
    return jsonify([item.serialize() for item in read_items]), 200


@app.route("/api/my-feeds/old")
@auth.login_required
def get_read_items_from_all_feeds():
    follow_relationships = Follows.query.filter_by(username=g.user.username).all()
    if not follow_relationships:
        return jsonify(f"User '{g.user.username}' does not follow any feeds")

    read_item_ids = []
    for relationship in follow_relationships:
        read_items = Read.query.filter_by(username=g.user.username, feed_id=relationship.feed_id).all()
        if read_items:
            for read_item in read_items:
                read_item_ids.append(read_item.item_id)

    unread_items = FeedItem.query.filter(FeedItem.id.in_(read_item_ids)).order_by(FeedItem.published.desc()).all()
    return jsonify([item.serialize() for item in unread_items]), 200


@app.route("/api/items/<item_id>/read", methods=["POST"])
@auth.login_required
def read_feed_item(item_id):
    item = FeedItem.query.get(item_id)
    if not item:
        log_and_raise(app.logger, FeedNotFound("Item id not found", 404, payload=request.json))

    follow_relationship = Follows.query.filter_by(username=g.user.username, feed_id=item.feed_id).first()
    if not follow_relationship:
        raise FeedNotFollowed(f"User '{g.user.username}' does not follow feed '{item.feed_id}'", status_code=409)

    unread = Unread.query.filter_by(username=g.user.username, item_id=item.id).first()
    read = Read(username=g.user.username, item_id=item.id, feed_id=item.feed_id)

    if unread:
        db.session.delete(unread)
    db.session.add(read)
    db.session.commit()
    return "", 204


@app.route("/api/items/read-multiple", methods=['POST'])
@auth.login_required
def read_multiple_feed_items():
    if request.json is None:
        raise MissingRequiredParameter("Missing request body.", 400, payload=request.json)
    item_ids = request.json.get('item_ids')
    if not item_ids:
        raise MissingRequiredParameter("Missing 'item_ids' in request body", 400, payload=request.json)

    feed_items = FeedItem.query.filter(FeedItem.id.in_(item_ids)).all()

    for feed_item in feed_items:
        unread = Unread.query.filter_by(username=g.user.username, item_id=feed_item.id).first()
        if unread:
            db.session.delete(unread)
            read = Read(username=g.user.username, item_id=feed_item.id, feed_id=feed_item.feed_id)
            db.session.add(read)

    db.session.commit()
    return "", 204


@app.route("/api/my-feeds/<feed_id>/update", methods=["POST"])
@auth.login_required
def refresh_single_feed(feed_id):
    feed = Feed.query.get(feed_id)
    if not feed:
        log_and_raise(app.logger, FeedNotFound("Feed id not found", 404, payload=request.json))

    try:
        scraper = Scraper({"url": feed.url, "parser": feed.parser, "time_format": feed.time_format})
        feed_items = scraper.parse()
        scraper.persist(feed_items)
    except Exception:
        raise InternalServerError("There was a problem updating the requested feed", 500, payload=request.json)
    else:
        scrape_single.delay(feed={"url": feed.url}, from_app=True, no_op=True)
        return jsonify({'message': 'Update successful'}), 200


@app.route("/api/my-feeds/update", methods=["POST"])
@auth.login_required
def refresh_all_user_feeds():
    follows = Follows.query.filter_by(username=g.user.username).all()
    feeds = Feed.query.filter(Feed.id.in_([item.feed_id for item in follows])).all()
    update_tasks = []
    for feed in feeds:
        try:
            scraper = Scraper({"url": feed.url, "parser": feed.parser, "time_format": feed.time_format})
            feed_items = scraper.parse()
            scraper.persist(feed_items)
        except Exception:
            update_tasks.append({"feed_id": f"{feed.id}", "status": "FAILED"})
        else:
            scrape_single.delay(feed={"url": feed.url}, from_app=True, no_op=True)
            update_tasks.append({"feed_id": f"{feed.id}", "status": "SUCCESSFUL"})

    return jsonify(update_tasks), 200


@auth.verify_password
def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user
    return True


@app.errorhandler(HTTPException)
def internal_server_error(error):
    db.session.rollback()
    response = error.get_response()
    response.data = json.dumps({
        "code": error.code,
        "name": error.name,
        "description": error.description
    })
    response.content_type = "application/json"
    return response


@app.route("/")
def hello():
    return "Hello there."
