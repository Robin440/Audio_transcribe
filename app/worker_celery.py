from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from pathlib import Path
from app.config import CELERY_BROKER_URL,CELERY_RESULT_BACKEND




celery_app = Celery('celery_app', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

# Import tasks here
from app.tasks.task import process_transcription

# Optional: You can also configure Celery settings here if needed
celery_app.conf.update(
    task_routes={
        'tasks.task.process_transcription': {'queue': 'default'},
    }
)
