import os

from flask_swagger_ui import get_swaggerui_blueprint


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


class Config(object):
    # -------- Celery --------
    beat_max_loop_interval = 600
    beat_schedule = {
        "regular_scrape": {
            "task": "scrape",
            "schedule": 30.0
        }
    }
    timezone = "UTC"

    # -------- Postgres --------

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

    # -------- Application --------
    SECRET_KEY = "totally_secret"


class TestConfig(Config):
    # -------- Celery --------
    broker_url = f"pyamqp://user:password@rabbitmq:5672//"

    # -------- Postgres --------
    SQLALCHEMY_DATABASE_URI = f"postgresql://postgres:dbpw@localhost:5432/feedaggregator_test"


class DevConfig(Config):
    # -------- Celery --------
    broker_url = f"pyamqp://user:password@rabbitmq:5672//"

    # -------- Postgres --------
    SQLALCHEMY_DATABASE_URI = f"postgresql://postgres:dbpw@localhost:5432/feedaggregator"

    # -------- Application --------
    debug = True


class ProdConfig(Config):
    broker_username = os.environ.get("RABBITMQ_USER")
    broker_password = os.environ.get("RABBITMQ_PASSWORD")
    broker_hostname = os.environ.get("BROKER_HOSTNAME")
    broker_port = os.environ.get("BROKER_PORT")

    PG_USER = os.environ.get("POSTGRES_USER")
    PG_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
    PG_DBNAME = os.environ.get("POSTGRES_DB")
    PG_PORT = os.environ.get("PG_PORT")

    # -------- Celery --------
    broker_url = f"pyamqp://{broker_username}:{broker_password}@{broker_hostname}:{broker_port}//"
    beat_schedule = {
        "regular_scrape": {
            "task": "scrape",
            "schedule": 600.0
        }
    }

    # -------- Postgres --------
    PG_HOST = "postgres"
    SQLALCHEMY_DATABASE_URI = f"postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DBNAME}"

    # -------- Server --------
    SECRET_KEY = os.urandom(32)
