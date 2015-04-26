from flask import Flask


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("common/config.py", silent=False)

    from extensions import db, celery

    db.init_app(app)
    celery.init_app(app)

    return app


