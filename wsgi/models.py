from extensions import db


class State(db.Model):
    state = db.Column(db.Boolean(), unique=True, primary_key=True)
    changed = db.Column(db.DateTime())

    def __init__(self, value, date):
        self.state = value
        self.changed = date


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


