from app import db


class regUser(db.Model):
    __tablename__ = "USERS"
    id = db.Column(db.Integer, primary_key=True)
    open_id = db.Column(db.String(30), unique=True)
    username = db.Column(db.String(30))
    password_urp = db.Column(db.String(30))
    password_drcom = db.Column(db.String(30))

    def __init__(self, openid, username, password_urp, password_drcom):
        self.openid = openid
        self.username = username
        self.password_urp = password_urp
        self.password_drcom = password_drcom

    def __repr__(self):
        return '<User %r>' % self.username
