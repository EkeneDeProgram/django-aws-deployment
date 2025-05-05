from .celery import app as celery_app

# Define __all__ to specify that 'celery_app' is the public object of this module
__all__ = ["celery_app"]