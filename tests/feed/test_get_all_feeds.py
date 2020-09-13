from tests import BaseTestFixture, basic_auth_headers


class TestSignup(BaseTestFixture):
    def test_get_all_feeds_when_not_authenticated(self):
        response = self.client.get('/api/feeds')
        self.assertEqual(401, response.status_code)

    def test_get_all_feeds_when_authenticated(self):
        response = self.client.get(
            '/api/feeds',
            headers=basic_auth_headers("user", "pass")
        )

        self.assertEqual(200, response.status_code)
