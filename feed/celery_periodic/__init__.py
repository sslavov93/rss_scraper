from celery import Celery

celery = None


def make_celery(main_flask_app):
    """Generates the celery object and ties it to the main Flask app object"""
    celery = Celery(main_flask_app.import_name, include=["feed.celery_periodic.tasks"])

    if main_flask_app.config["ENV"] == "production":
        conf = "config.ProdConfig"
    else:
        conf = "config.DevConfig"

    celery.config_from_object(conf)

    task_base = celery.Task

    class ContextTask(task_base):
        abstract = True

        def __call__(self, *args, **kwargs):
            with main_flask_app.app_context():
                return task_base.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery
