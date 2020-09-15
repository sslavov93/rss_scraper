#!/bin/bash

sleep 20
celery -A feed.celery_periodic.worker.celery beat -l info &
celery -A feed.celery_periodic.worker.celery worker -l info &
gunicorn --bind 0.0.0.0:5000 application:app