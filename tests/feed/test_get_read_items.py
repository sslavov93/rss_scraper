from feed.models import Unread
from tests import BaseTestFixture, basic_auth_headers


class TestGetReadItems(BaseTestFixture):
    def test_get_read_items_from_feed_no_auth(self):
        response = self.client.get('/api/my-feeds/1/old')
        self.assertEqual(401, response.status_code)

    def test_get_read_items_from_feed_when_feed_is_missing(self):
        response = self.client.get(
            '/api/my-feeds/5/old',
            headers=basic_auth_headers("user", "pass")
        )
        self.assertEqual(404, response.status_code)

    def test_get_read_items_from_feed_if_not_followed(self):
        response = self.client.get(
            '/api/my-feeds/1/old',
            headers=basic_auth_headers("user3", "pass")
        )
        self.assertEqual("User 'user3' does not follow feed '1'", response.get_json().get("message"))
        self.assertEqual(409, response.status_code)

    def test_get_read_items_from_feed_no_error(self):
        response = self.client.get(
            '/api/my-feeds/1/old',
            headers=basic_auth_headers("user", "pass")
        )
        with self.app.app_context():
            unreads = Unread.query.filter_by(username='user', feed_id=1).all()
            self.assertEqual(1, len(unreads))

        self.assertEqual(200, response.status_code)

    def test_get_all_read_items_no_auth(self):
        response = self.client.get('/api/my-feeds/old')
        self.assertEqual(401, response.status_code)

    def test_get_all_read_items_when_user_follows_no_feed(self):
        response = self.client.get(
            '/api/my-feeds/old',
            headers=basic_auth_headers("user3", "pass")
        )
        self.assertEqual("User 'user3' does not follow any feeds", response.get_json())
        self.assertEqual(200, response.status_code)

    def test_get_all_read_items_when_user_follows_some_feeds(self):
        response = self.client.get(
            '/api/my-feeds/old',
            headers=basic_auth_headers("user", "pass")
        )
        with self.app.app_context():
            unreads = Unread.query.filter_by(username='user').all()
            self.assertEqual(1, len(unreads))

        self.assertEqual(200, response.status_code)
