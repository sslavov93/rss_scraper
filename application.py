from feed import create_app
from feed.celery_periodic import make_celery



app = create_app()
app.celery = make_celery(app)


if __name__ == "__main__":
    app.run()
