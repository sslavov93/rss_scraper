from feed import celery_periodic, create_app


app = create_app()
celery = celery_periodic.make_celery(app)
celery_periodic.celery = celery
