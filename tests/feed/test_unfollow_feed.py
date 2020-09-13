from feed.models import Unread
from tests import BaseTestFixture, basic_auth_headers


class TestUnfollowFeed(BaseTestFixture):
    def test_unfollow_feed_if_feed_not_exist(self):
        response = self.client.delete(
            '/api/feeds/unfollow',
            headers=basic_auth_headers("user", "pass"),
            json={"feed_id": 5}
        )
        self.assertEqual(404, response.status_code)

    def test_unfollow_feed_if_followed(self):
        response = self.client.delete(
            '/api/feeds/unfollow',
            headers=basic_auth_headers("user2", "pass"),
            json={"feed_id": 2}
        )
        with self.app.app_context():
            unreads = Unread.query.filter_by(username="user2").all()

        self.assertEqual(0, len(unreads))
        self.assertEqual(204, response.status_code)

    def test_unfollow_feed_if_not_following(self):
        response = self.client.delete(
            '/api/feeds/unfollow',
            headers=basic_auth_headers("user2", "pass"),
            json={"feed_id": 1}
        )
        self.assertEqual(409, response.status_code)

    def test_unfollow_feed_if_bad_request(self):
        response = self.client.delete(
            '/api/feeds/unfollow',
            headers=basic_auth_headers("user2", "pass"),
            json={"something": 1}
        )
        self.assertEqual(400, response.status_code)

    def test_unfollow_feed_if_not_authenticated(self):
        response = self.client.delete('/api/feeds/unfollow', json={"feed_id": 1})
        self.assertEqual(401, response.status_code)

    def test_unfollow_feed_no_request_body(self):
        response = self.client.delete('/api/feeds/unfollow', headers=basic_auth_headers("user2", "pass"))
        self.assertEqual(400, response.status_code)
