from app import db

class regUser(db.Model):
    __tablename__ = "user"
    openid = db.Column(db.String(80), primary_key = True)
    username = db.Column(db.String(80), unique=True)
    password_urp = db.Column(db.String(256))
    password_drcom = db.Column(db.String(256))

    def __init__(self, openid, username, password_urp, password_drcom):
        self.openid   = openid
        self.username = username
        self.password_urp = password_urp
	self.password_drcom = password_drcom
	
    def __repr__(self):
        return '<User %r - %r - %r>' % (self.username,self.password_urp,self.password_drcom)


