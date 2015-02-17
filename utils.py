import os
import sqlite3 as lite

from wsgi.common import constants


__author__ = 'aguzun'


def camera_not_configured():
    print "Please setup your camera"


def get_cam_config():
    if constants.Environment.DB_PATH not in os.environ:
        os.environ[constants.Environment.DB_PATH] = '/tmp/webcam.db'
    try:
        conn = lite.connect(os.environ.get(constants.Environment.DB_PATH))
        c = conn.cursor()
        c.execute('select * from Config')
        config = {}
        for _id, value, description in c.fetchall():
            config[_id] = value
        c.close()
        conn.close()

        return config
    except Exception, e:
        print e
        return None