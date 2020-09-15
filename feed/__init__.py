from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from feed import celery_periodic

db = SQLAlchemy()
migrate = Migrate()
auth = HTTPBasicAuth()

envs = {
    "production": "config.ProdConfig",
    "development": "config.DevConfig",
    "testing": "config.TestConfig",
}


def create_app():
    """Construct the main Flask application with all submodules and dependencies"""
    app = Flask(__name__, instance_relative_config=False)

    app.config.from_object(envs.get(app.config.get("ENV"), "config.DevConfig"))

    db.init_app(app)
    migrate.init_app(app, db)

    celery = celery_periodic.make_celery(app)
    celery_periodic.celery = celery

    app.register_blueprint(app.config.get("SWAGGERUI_BLUEPRINT"), url_prefix=app.config.get("SWAGGER_URL"))

    with app.app_context():
        from . import routes

    return app
