from feed import create_app
from feed.celery_periodic import make_celery

app = create_app()
if app.config["ENV"] == "production":
    conf = "config.ProdConfig"
else:
    conf = "config.DevConfig"

app.config.from_object(conf)

app.celery = make_celery(app)


if __name__ == "__main__":
    app.run()
