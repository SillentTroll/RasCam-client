from urlparse import urljoin

import requests
import simplejson

from common import constants

API_KEY_PARAMETER = "api_key"

from requests.auth import AuthBase


class BearerAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['Authorization'] = 'Bearer ' + self.token
        return r


def handle_server_response(response_json):
    if 'description' in response_json:
        raise Exception(response_json.get('description'))
    elif 'error' in response_json:
        raise Exception(response_json.get('error'))
    raise Exception('Server is not properly configured. See the documentation')


def register_cam(server_url, cam_name, username, password):
    try:
        auth_payload = {
            'username': username,
            'password': password
        }
        auth_response = requests.post(urljoin(server_url, constants.Backend.AUTH_URL),
                                      data=simplejson.dumps(auth_payload), timeout=10)
    except Exception, e:
        print e.message
        raise Exception("Could not connect to server")

    if not auth_response or auth_response.status_code != requests.codes.ok or 'token' not in auth_response.json():
        handle_server_response(auth_response.json())
    else:
        json = auth_response.json()

        payload = {
            'cam_name': cam_name,
        }
        auth = BearerAuth(json.get('token'))

        response = requests.put(urljoin(server_url, constants.Backend.REGISTER_CAM_URL), data=payload,
                                auth=auth)
        response_json = response.json()
        if response.status_code == requests.codes.ok:
            return response_json.get(API_KEY_PARAMETER)
        else:
            handle_server_response(response_json)

