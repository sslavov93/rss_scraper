from tests import BaseTestFixture


class TestSignup(BaseTestFixture):
    def test_successful_signup(self):
        payload = {
            "username": "test",
            "password": "test"
        }

        response = self.client.post('/api/users', json=payload)

        self.assertEqual('test', response.json['username'])
        self.assertEqual(201, response.status_code)

    def test_signup_no_password(self):
        payload = {
            "username": "test"
        }

        response = self.client.post('/api/users', json=payload)

        self.assertEqual(400, response.status_code)

    def test_signup_no_username(self):
        payload = {
            "password": "test"
        }
        response = self.client.post('/api/users', json=payload)
        self.assertEqual(400, response.status_code)

    def test_signup_user_already_exists(self):
        payload = {
            "password": "test"
        }
        response = self.client.post('/api/users', json=payload)
        self.assertEqual(400, response.status_code)

    def test_signup_no_request_body(self):
        response = self.client.post('/api/users')
        self.assertEqual(400, response.status_code)
