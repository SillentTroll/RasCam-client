__author__ = 'aguzun'

from urlparse import urljoin

import requests


class ControlOption(object):
    def __init__(self, option_name):
        self.option_name = option_name
        self.control_url = "http://localhost:8080"  # change the port in motion.config
        self.thread_nr = "0"  # multiple cameras can be connected. For now only one is supported.

    def execute(self, option_name, command):
        params = [self.thread_nr, option_name, command]
        url = urljoin(self.control_url, "/".join(params))
        print url
        response = requests.get(url)
        if response.status_code == requests.codes.ok:
            return str(response.text)
        else:
            return None


class Detection(ControlOption):
    def __init__(self):
        ControlOption.__init__(self, "detection")

    def get_status(self):
        response_text = self.execute(self.option_name, "status")
        if "PAUSE" in response_text:
            return False
        elif "ACTIVE" in response_text:
            return True
        else:
            print "Got an invalid response %s" % response_text
            return None

    def start(self):
        return self.execute(self.option_name, "start")

    def pause(self):
        return self.execute(self.option_name, "pause")


class Action(ControlOption):
    def __init__(self):
        ControlOption.__init__(self, "action")

    def take_snapshot(self):
        return self.execute(self.option_name, "snapshot")


detection = Detection()
