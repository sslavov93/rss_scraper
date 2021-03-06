from unittest.mock import patch

from feed.models import FeedItem
from tests import BaseTestFixture, basic_auth_headers


class TestRefreshUserFeeds(BaseTestFixture):
    def test_refresh_single_feed_when_not_authenticated(self):
        response = self.client.post('/api/my-feeds/5/update')
        self.assertEqual(401, response.status_code)

    def test_refresh_all_user_feeds_when_not_authenticated(self):
        response = self.client.post('/api/my-feeds/update')
        self.assertEqual(401, response.status_code)

    def test_refresh_single_feed_when_feed_not_exist(self):
        response = self.client.post(
            '/api/my-feeds/5/update',
            headers=basic_auth_headers("user", "pass")
        )
        self.assertEqual(404, response.status_code)

    @patch("feed.routes.Scraper")
    @patch("feed.routes.scrape_single")
    def test_refresh_single_feed_no_error(self, scrape_single_task, scraper):
        scraper.parse.return_value = [FeedItem(id=5), FeedItem(id=6)]
        scrape_single_task.return_value = {}

        response = self.client.post(
            '/api/my-feeds/1/update',
            headers=basic_auth_headers("user", "pass")
        )

        self.assertEqual(200, response.status_code)
        self.assertTrue(scraper.persist.called_with([FeedItem(id=5), FeedItem(id=6)]))
        self.assertTrue(scrape_single_task.delay.called)

    @patch("feed.routes.Scraper")
    @patch("feed.routes.scrape_single")
    def test_refresh_all_user_feeds_no_error(self, scrape_single_task, scraper):
        scraper.parse.return_value = [FeedItem(id=5), FeedItem(id=6)]
        scrape_single_task.return_value = {}

        response = self.client.post(
            '/api/my-feeds/update',
            headers=basic_auth_headers("user", "pass")
        )

        self.assertEqual(200, response.status_code)
        self.assertTrue(scraper.persist.called_with([FeedItem(id=5), FeedItem(id=6)]))
        self.assertTrue(scrape_single_task.delay.called)
