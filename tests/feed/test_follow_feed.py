from feed.models import Unread
from tests import BaseTestFixture, basic_auth_headers


class TestFollowFeed(BaseTestFixture):
    def test_follow_feed_if_feed_not_exist(self):
        response = self.client.post(
            '/api/feeds/follow',
            headers=basic_auth_headers("user", "pass"),
            json={"feed_id": 5}
        )
        self.assertEqual(404, response.status_code)

    def test_follow_feed_if_not_followed(self):
        response = self.client.post(
            '/api/feeds/follow',
            headers=basic_auth_headers("user", "pass"),
            json={"feed_id": 2}
        )
        with self.app.app_context():
            unreads = Unread.query.filter_by(username="user").all()

        self.assertEqual(3, len(unreads))
        self.assertEqual(204, response.status_code)

    def test_follow_feed_if_already_followed(self):
        response = self.client.post(
            '/api/feeds/follow',
            headers=basic_auth_headers("user", "pass"),
            json={"feed_id": 1}
        )
        self.assertEqual(409, response.status_code)

    def test_follow_feed_if_bad_request(self):
        response = self.client.post(
            '/api/feeds/follow',
            headers=basic_auth_headers("user", "pass"),
            json={"something": 1}
        )
        self.assertEqual(400, response.status_code)

    def test_follow_feed_if_not_authenticated(self):
        response = self.client.post('/api/feeds/follow', json={"feed_id": 1})
        self.assertEqual(401, response.status_code)

    def test_follow_feed_no_request_body(self):
        response = self.client.post('/api/feeds/follow', headers=basic_auth_headers("user", "pass"))
        self.assertEqual(400, response.status_code)
