from functools import wraps
import os

from flask import (Flask, url_for, request, render_template, flash, jsonify)
from werkzeug.utils import redirect
from wtforms import Form, TextField, validators, PasswordField

from flask.ext.sqlalchemy import SQLAlchemy
import back_end_services
from common import constants


app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(126)

CONF_SERVER_URL = 'SERVER_URL'
CONF_IS_CONFIGURED = 'IS_CONFIGURED'

if constants.Environment.SQLLITE_DB_PATH not in os.environ:
    os.environ[constants.Environment.SQLLITE_DB_PATH] = constants.Environment.DB_PATH

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.environ.get(constants.Environment.SQLLITE_DB_PATH)

db = SQLAlchemy(app)


def requires_valid_config(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if get_backend_url():
            return f(*args, **kwargs)
        else:
            return redirect(url_for("first_config"))

    return decorated_function


class Config(db.Model):
    id = db.Column(db.String(80), unique=True, primary_key=True)
    value = db.Column(db.String(300))
    desc = db.Column(db.String(100))

    def __init__(self, id, value, desc):
        self.id = id
        self.value = value
        self.desc = desc

    def __repr__(self):
        return '<Config %r:%r>' % (self.id, self.value)


db.create_all()


@app.route("/")
def index():
    if get_backend_url():
        return redirect(url_for('settings'))
    else:
        return redirect(url_for('first_config'))


@app.route("/config", methods=['GET', 'POST'])
def first_config():
    if not get_backend_url():
        form = FirstStepForm(request.form)
        if request.method == "POST" and form.validate():
            try:
                api_key = back_end_services.register_cam(form.url.data, form.cam_name.data,
                                                         form.username.data,
                                                         form.password.data)
            except Exception, e:
                flash(e.message)
                return render_template('config.html', form=form)

            if api_key:
                db.session.add(Config(constants.Config.SERVER_URL, form.url.data, "The URL of the server"))
                db.session.add(Config(constants.Config.CAMERA_NAME, form.cam_name.data, "The name of the camera"))
                db.session.add(Config(constants.Config.API_KEY, api_key, "Api key"))
                db.session.commit()
                return redirect(url_for('index'))
        else:
            return render_template('config.html', form=form)

    return redirect(url_for('index'))


class FirstStepForm(Form):
    url = TextField("The URL of the server",
                    [validators.required(message="Without the sever, camera will not work"),
                     validators.url], default="http://")
    username = TextField("The server username",
                         [validators.required(message="Server requires authentication!")])
    password = PasswordField("The server password",
                             [validators.required(message="Server requires authentication!")])
    cam_name = TextField("The name of the camera",
                         [validators.required(message="Everyone should have a name!")])


@app.route("/settings")
@requires_valid_config
def settings():
    configs = []
    for config in Config.query.all():
        configs.append({
            "id": config.id,
            "value": config.value,
            "desc": config.desc
        })
    return render_template("settings.html", settings=configs)


@app.route("/reset", methods=['GET'])
@requires_valid_config
def reset_camera():
    if not request.args.get('confirmation') or not request.args.get('camera_name'):
        return jsonify(result="NOK", error="Invalid camera name")
    else:
        if request.args.get('camera_name') == get_webcam_name():
            for config in Config.query.all():
                db.session.delete(config)
            db.session.commit()
            return jsonify(result="OK")
        else:
            return jsonify(result="NOK", error="Invalid camera name")


def get_backend_url():
    return get_config_from_db(constants.Config.SERVER_URL)


def get_webcam_name():
    return get_config_from_db(constants.Config.CAMERA_NAME)


def get_config_from_db(config_id):
    from_db = Config.query.filter_by(id=config_id).first()
    if not from_db:
        return None
    else:
        return from_db.value


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
