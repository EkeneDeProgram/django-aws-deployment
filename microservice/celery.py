# Standard library imports
import os

# Related third-party imports
from celery import Celery

# Set the default Django settings module for the 'celery'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "microservice.settings")

# Create a Celery app instance with the name 'microservice'.
app = Celery("microservice")

# Load configuration from Django settings using the 'CELERY_' prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Automatically discover and load tasks from all registered Django app configs.
app.autodiscover_tasks()
