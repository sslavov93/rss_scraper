import os

from fabric import task
from invoke import run

from feed import create_app, db
from sqlalchemy_utils import database_exists, create_database, drop_database


@task
def test(context, env='testing'):
    os.environ['FLASK_ENV'] = env
    run("coverage run --source=tests/ -m pytest ")


@task
def docs(context):
    pass


@task
def serve(context):
    run("flask run --host=0.0.0.0")


@task
def init(context, env="development"):
    init_rabbitmq()
    init_db()


@task
def init_rabbitmq(context, env="development"):
    run("docker exec -it rabbitmq rabbitmqctl add_user user password 2>/dev/null ")
    run("docker exec -it rabbitmq rabbitmqctl set_user_tags user administrator")
    run("docker exec -it rabbitmq rabbitmqctl set_permissions -p / user  \".*\" \".*\" \".*\"")


@task
def init_db(context, env='development'):
    from tests.utils import generate_setup
    os.environ['FLASK_ENV'] = env

    url = "postgresql://postgres:dbpw@localhost:5432/feedaggregator"
    url += "" if env != 'testing' else "_test"

    if database_exists(url):
        print("dropping")
        drop_database(url)
    print("creating")
    create_database(url)

    app = create_app()
    with app.app_context():
        db.create_all()
        items = generate_setup()
        db.session.add_all(items)
        db.session.commit()
        print("DONE.")


@task
def migratedb(context):
    run("python3 manage.py db migrate")
    run("python3 manage.py db upgrade")
