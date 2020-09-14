from celery import Celery

celery = None

envs = {
    "production": "config.ProdConfig",
    "development": "config.DevConfig",
    "testing": "config.TestConfig",
}

def make_celery(main_flask_app):
    """Generates the celery object and ties it to the main Flask app object"""
    celery = Celery(main_flask_app.import_name, include=["feed.celery_periodic.tasks"])

    celery.config_from_object(envs.get(main_flask_app.config.get("ENV"), "config.DevConfig"))

    task_base = celery.Task

    class ContextTask(task_base):
        abstract = True

        def __call__(self, *args, **kwargs):
            with main_flask_app.app_context():
                return task_base.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery
