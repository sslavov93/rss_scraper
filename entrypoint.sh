#!/bin/bash

celery -A feed.celery_periodic.worker.celery beat -l debug &
celery -A feed.celery_periodic.worker.celery worker -l debug &
fab serve
