from celery.utils.log import get_task_logger
from feed import create_app
from feed.celery_periodic import make_celery

app = create_app()
if app.config["ENV"] == "production":
    conf = "config.ProdConfig"
else:
    conf = "config.DevConfig"

app.config.from_object(conf)
logger = get_task_logger(__name__)

app.celery = make_celery(app)


if __name__ == "__main__":
    app.run(ssl_context="adhoc", host="0.0.0.0", port=5000, debug=True)
