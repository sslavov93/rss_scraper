from feed.models import Unread
from tests import BaseTestFixture, basic_auth_headers


class TestReadFeedItems(BaseTestFixture):
    def test_read_single_item_when_not_authenticated(self):
        response = self.client.post('/api/items/1/read')
        self.assertEqual(401, response.status_code)

    def test_read_single_item_when_item_not_exists(self):
        response = self.client.post(
            '/api/items/5/read',
            headers=basic_auth_headers("user", "pass")
        )
        self.assertEqual(404, response.status_code)

    def test_read_single_item_when_feed_is_not_followed(self):
        response = self.client.post(
            '/api/items/1/read',
            headers=basic_auth_headers("user3", "pass")
        )
        self.assertEqual(409, response.status_code)

    def test_read_single_item_no_error(self):
        response = self.client.post(
            '/api/items/1/read',
            headers=basic_auth_headers("user", "pass")
        )

        with self.app.app_context():
            unreads = Unread.query.filter_by(username="user", feed_id=1).all()
            self.assertEqual(0, len(unreads))

        self.assertEqual(204, response.status_code)

    def test_read_multiple_items_when_not_authenticated(self):
        response = self.client.post('/api/items/read-multiple')
        self.assertEqual(401, response.status_code)

    def test_read_multiple_items_missing_parameter(self):
        response = self.client.post(
            '/api/items/read-multiple',
            headers=basic_auth_headers("user", "pass")
        )

        self.assertEqual(400, response.status_code)

    def test_read_multiple_items_no_error(self):
        response = self.client.post(
            '/api/items/read-multiple',
            headers=basic_auth_headers("user2", "pass"),
            json={'item_ids': ['3', '4']}
        )

        with self.app.app_context():
            unreads = Unread.query.filter_by(username="user2", feed_id=2).all()
            self.assertEqual(0, len(unreads))

        self.assertEqual(204, response.status_code)
