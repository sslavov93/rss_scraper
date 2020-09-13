from flask_swagger_ui import get_swaggerui_blueprint


class Config:
    # backend = "rpc://"
    broker_url = "pyamqp://user:password@localhost:5672//"

    beat_max_loop_interval = 600
    beat_schedule = {
        "regular_scrape": {
            "task": "scrape",
            "schedule": 30.0
        }
    }
    timezone = "UTC"

    feeds = [
        {
            "id": 2,
            "url": "http://www.nu.nl/rss/Algemeen",
            "parser": "lxml",
            "time_format": "%a, %d %b %Y %H:%M:%S %z"
        },
        {
            "id": 1,
            "url": "https://feeds.feedburner.com/tweakers/mixed",
            "parser": "html5lib",
            "time_format": "%a, %d %b %Y %H:%M:%S %Z"
        },
    ]

    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:dbpw@localhost:5432/feedaggregator"
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SECRET_KEY = "totally_secret"

    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "RSS-Feed-Aggregator"
        }
    )


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:dbpw@localhost:5432/feedaggregator_test"


class DevConfig(Config):
    debug = True


class ProdConfig(Config):
    broker_url = "pyamqp://user:password@localhost:5672//"

    beat_schedule = {
        "regular_scrape": {
            "task": "scrape",
            "schedule": 600.0
        }
    }
    timezone = "UTC"

    feeds = [
        {
            "url": "http://www.nu.nl/rss/Algemeen",
            "parser": "lxml",
            "time_format": "%a, %d %b %Y %H:%M:%S %z"
        },
        {
            "url": "https://feeds.feedburner.com/tweakers/mixed",
            "parser": "html5lib",
            "time_format": "%a, %d %b %Y %H:%M:%S %Z"
        },
    ]

    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:dbpw@postgres:5432/feedaggregator"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
