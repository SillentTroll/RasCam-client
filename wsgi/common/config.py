import os
from datetime import timedelta


SECRET_KEY = os.urandom(126)

SQLALCHEMY_DATABASE_URI = "sqlite:////var/data/webcam.db"

CELERYBEAT_SCHEDULE = {
    'check-state': {
        'task': 'camera_worker.check_state',
        'schedule': timedelta(seconds=30),
    },
}
CELERY_TASK_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']  # Ignore other content
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Lisbon'
CELERY_ENABLE_UTC = True
