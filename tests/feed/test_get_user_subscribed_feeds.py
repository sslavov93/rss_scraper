from tests import BaseTestFixture, basic_auth_headers


class TestGetUserSubscribedFeeds(BaseTestFixture):
    def test_get_user_feeds_without_auth(self):
        response = self.client.get('/api/my-feeds')
        self.assertEqual(401, response.status_code)

    def test_get_user_feeds_with_auth_and_no_feeds_present(self):
        response = self.client.get(
            '/api/my-feeds',
            headers=basic_auth_headers("user3", "pass")
        )

        resp_content = response.get_json()
        self.assertEqual(200, response.status_code)
        self.assertEqual([], resp_content)

    def test_get_user_feeds_with_auth_and_feeds_present(self):
        response = self.client.get(
            '/api/my-feeds',
            headers=basic_auth_headers("user", "pass")
        )

        resp_content = response.get_json()
        self.assertEqual(200, response.status_code)
        self.assertEqual([{'id': 1, 'url': 'https://feeds.feedburner.com/tweakers/mixed'}], resp_content)
