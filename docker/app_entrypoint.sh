#!/bin/bash

sleep 20
celery -A feed.celery_periodic.worker.celery beat -l debug &
celery -A feed.celery_periodic.worker.celery worker -l debug &
gunicorn --bind 0.0.0.0:5000 application:app