from celery import Celery
from celery import current_app as current_celery_app
from flask import Flask

from src.config import settings


def make_celery(app: Flask) -> Celery:
    celery = current_celery_app
    celery.config_from_object(app.config, namespace="CELERY")
    celery.conf.update(
        result_backend=settings.CELERY_BROKER_URL,
        broker_url=settings.CELERY_RESULT_BACKEND,
    )

    return celery
