from flask_swagger_ui import get_swaggerui_blueprint


class Config:
    # -------- Celery --------
    broker_username = "user"
    broker_password = "password"
    broker_hostname = "localhost"
    broker_port = "5672"

    broker_url = f"pyamqp://{broker_username}:{broker_password}@{broker_hostname}:{broker_port}//"
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

    # -------- Postgres --------
    PG_USER = "postgres"
    PG_PASSWORD = "dbpw"
    PG_HOST = "localhost"
    PG_PORT = "5432"
    PG_DBNAME = "feedaggregator"

    SQLALCHEMY_DATABASE_URI = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DBNAME}"
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # -------- Swagger API Blueprint --------
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "RSS-Feed-Aggregator"
        }
    )

    SECRET_KEY = "totally_secret"


class TestConfig(Config):
    PG_USER = "postgres"
    PG_PASSWORD = "dbpw"
    PG_HOST = "localhost"
    PG_PORT = "5432"
    PG_DBNAME = "feedaggregator_test"
    SQLALCHEMY_DATABASE_URI = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DBNAME}"
    # SQLALCHEMY_DATABASE_URI = "postgresql://postgres:dbpw@localhost:5432/feedaggregator_test"


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
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
