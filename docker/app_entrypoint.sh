#!/bin/bash

gunicorn --bind 0.0.0.0:5000 application:app &
sleep 10
celery -A feed.celery_periodic.worker.celery beat -l debug &
sleep 10
celery -A feed.celery_periodic.worker.celery worker -l debug &
