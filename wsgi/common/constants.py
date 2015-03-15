class Config(object):
    SERVER_URL = "BACKEND_SERVER_URL"
    CAMERA_NAME = "CAM_NAME"
    API_KEY = "API_KEY"
    IP = "IP"


class Environment(object):
    SQLLITE_DB_PATH = "SQLITE_DB_PATH"
    DB_PATH = "/var/data/webcam.db"


class Backend(object):
    URL_PREFIX = "http://"
    API_PREFIX = "/api/v1/"
    AUTH_URL = "%susers/auth" % API_PREFIX
    REGISTER_CAM_URL = "%scam" % API_PREFIX
    UPLOAD_URL = "%scam/upload" % API_PREFIX
    CHECK_STATE = "%scam/state" % API_PREFIX
