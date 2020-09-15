#!/bin/bash

mkdir -p /var/run/celery /var/log/celery
touch /celerybeat.pid
chown -R nobody:nogroup /var/run/celery /var/log/celery /celerybeat.pid

sleep 20
celery -A feed.celery_periodic.worker.celery beat -l debug --uid=nobody --gid=nogroup &
celery -A feed.celery_periodic.worker.celery worker -l debug --uid=nobody --gid=nogroup &
gunicorn --bind 0.0.0.0:5000 application:app