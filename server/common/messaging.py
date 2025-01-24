from celery import Celery

from config import get_settings
from user.application.send_welcome_email_task import SendWelcomeEmailTask

import eventlet
eventlet.monkey_patch()

settings = get_settings()

celery = Celery(
    "TIL",
    broker=settings.celery_broker_url,
    backend=settings.celery_backend_url,
    broker_connection_retry_on_startup=True,
    include=["user.application.send_welcome_email_task"]
)

celery.register_task(SendWelcomeEmailTask())