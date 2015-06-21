import os
from urlparse import urljoin

import requests

from motion import motion_control
from datetime import datetime
from wsgi.common import constants
from wsgi.extensions import celery as worker, db
from wsgi.server import get_config_from_db, get_camera_state


def get_config_data():
    url = get_config_from_db(constants.Config.SERVER_URL)
    api_key = get_config_from_db(constants.Config.API_KEY)
    if not url or not api_key:
        camera_not_configured()
        return None, None
    else:
        return url, api_key


@worker.task
def check_state():
    url, api_key = get_config_data()
    camera_state = get_camera_state()
    if url and api_key:
        params = {
            'api_key': api_key,
        }
        response = requests.get(urljoin(url, constants.Backend.CHECK_STATE), params=params)
        if response.status_code == requests.codes.ok:
            result_json = response.json()
            if "camera_state" in result_json:
                new_state = result_json.get("camera_state")
                if new_state != camera_state.state:
                    print "Got new state : %s" % new_state
                    camera_state.state = new_state
                    camera_state.changed = datetime.now()
                    db.session.commit()
                    if new_state:
                        motion_control.detection.start()
                    else:
                        motion_control.detection.pause()
        else:
            print "Server returned %s", response.status_code


@worker.task(retry_count=15)
def upload(filename, date, remove):
    url, api_key = get_config_data()
    camera_state = get_camera_state()

    if url and api_key and camera_state.state:
        print "Uploading image %s" % filename

        files = {'file': (filename, open(filename, 'rb'))}
        payload = {
            'date': date,
            'api_key': api_key
        }
        response = requests.post(urljoin(url, constants.Backend.UPLOAD_URL), files=files, data=payload)
        if response.status_code == requests.codes.ok:
            response_json = response.json()
            if response_json.get('status') == "OK" and remove:
                os.remove(filename)
                print "File %s removed after upload" % filename

            if "camera_state" in response_json and response_json.get("camera_state") is False:
                print "Camera was deactivated, changing the state in DB"
                motion_control.detection.pause()
                camera_state.state = False
                camera_state.changed = datetime.now()
                db.session.commit()
        else:
            print "Server returned %s", response.status_code
    else:
        raise upload.retry(countdown=60 * 5)


def camera_not_configured():
    print "Please setup your camera first"