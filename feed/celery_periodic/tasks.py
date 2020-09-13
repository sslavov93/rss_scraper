from celery.utils.log import get_task_logger
from sqlalchemy.exc import SQLAlchemyError

from feed import celery_periodic
from feed.celery_periodic.default_scraper import DefaultParser

celery = celery_periodic.celery
logger = get_task_logger(__name__)


FORBIDDEN = set()


@celery.task(bind=True, name="scrape")
def scrape(self):
    for rss_feed in celery.conf.feeds:
        if rss_feed['url'] not in FORBIDDEN:
            logger.info(f"Scraping feed {rss_feed['url']} for new items...")
            scrape_single.s(rss_feed["url"]).delay()
        else:
            logger.info(f"Feed {rss_feed['url']} is not auto-updating")


@celery.task(bind=True, name="scrape_single", retry_kwargs={'max_retries': 5}, retry_backoff=5.0, retry_jitter=True)
def scrape_single(self, feed_url, from_app=False):
    if from_app:
        logger.info("Execution triggered from Flask App")
    try:
        parser = DefaultParser(feed_url)
        parser.persist()
        if feed_url in FORBIDDEN:
            FORBIDDEN.remove(feed_url)
    except ConnectionError as err:
        FORBIDDEN.add(feed_url)
        raise err
    except (AttributeError, KeyError) as err:
        FORBIDDEN.add(feed_url)
        raise err
    except SQLAlchemyError as err:
        FORBIDDEN.add(feed_url)
        raise err
    except Exception:
        FORBIDDEN.add(feed_url)
        raise
