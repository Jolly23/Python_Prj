import os
import sys

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.bcrypt import Bcrypt
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment



app = Flask(__name__)
app.config.from_object('config')
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
bootstrap=Bootstrap(app)
moment = Moment(app)

db.engine.pool._use_threadlocal = True

def register_blueprints():

    from app.user.views import user
    from app.weixin.views import weixin
    from app.admin.views import manage
    from app.lovewall import lovewall

    app.register_blueprint(user)
    app.register_blueprint(weixin)
    app.register_blueprint(manage)
    app.register_blueprint(lovewall)

register_blueprints()
