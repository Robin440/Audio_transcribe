from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

broker_url = os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/0')
result_backend = os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')

celery_app = Celery('celery_app', broker=broker_url, backend=result_backend)

# Import tasks here
from tasks.task import process_transcription

# Optional: You can also configure Celery settings here if needed
celery_app.conf.update(
    task_routes={
        'tasks.task.process_transcription': {'queue': 'default'},
    }
)
