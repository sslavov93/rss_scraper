import webbrowser

from fabric import task
from invoke import run


@task
def test(context):
    run("FLASK_ENV=testing coverage run --source=tests/ -m pytest ")


@task
def docs(context):
    webbrowser.open("http://localhost:1337/swagger", new=2)


@task
def serve(context):
    run("flask run --host=127.0.0.1 --port=5000")


@task
def migratedb(context):
    run("python3 manage.py db migrate")
    run("python3 manage.py db upgrade")


@task
def initdb(context):
    run("python3 manage.py init_db")
