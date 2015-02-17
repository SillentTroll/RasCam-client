import os


__author__ = 'aguzun'

from urlparse import urljoin
from datetime import timedelta

import requests
from celery import Celery

from motion import motion_control
from wsgi.common import constants
import utils

worker = Celery('tasks', broker='amqp://guest@localhost//')

worker.conf.update(
    CELERYBEAT_SCHEDULE={
        'add-every-30-seconds': {
            'task': 'camera_worker.check_state',
            'schedule': timedelta(seconds=30),
        },
    },
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],  # Ignore other content
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Europe/Lisbon',
    CELERY_ENABLE_UTC=True,
)


def get_config_data():
    config = utils.get_cam_config()
    if config:
        url = config[constants.Config.SERVER_URL]
        api_key = config[constants.Config.API_KEY]
        if not url or not api_key:
            utils.camera_not_configured()
            return None, None
        else:
            return url, api_key
    else:
        utils.camera_not_configured()
        return None, None


@worker.task
def check_state():
    print "Going to check the state"
    url, api_key = get_config_data()

    if url and api_key:
        params = {
            'api_key': api_key,
        }
        response = requests.get(urljoin(url, constants.Backend.CHECK_STATE), params=params)
        if response.status_code == requests.codes.ok:
            result_json = response.json()
            result_state = result_json.get("state")
            print "Got state : %s" % result_state
            if result_state is not None:
                if result_state:
                    motion_control.detection.start()
                else:
                    motion_control.detection.pause()
            if result_json.get("config_changed"):
                print "server config changed, going to update the config"
                # TODO update the config
        else:
            print "Server returned %s", response.status_code


@worker.task
def upload(filename, date, event, remove):
    url, api_key = get_config_data()

    if url and api_key:
        files = {'file': (filename, open(filename, 'rb'))}
        payload = {
            'date': date,
            'event': event,
            'api_key': api_key
        }
        response = requests.post(urljoin(url, constants.Backend.UPLOAD_URL), files=files, data=payload)
        if response.status_code == requests.codes.ok:
            if remove and response.json().get('status') == "OK":
                os.remove(filename)
                print "File %s removed after upload" % filename
        else:
            print "Server returned %s", response.status_code
    else:
        raise upload.retry(countdown=60 * 5)






