from flask import Flask, render_template, redirect, url_for
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from flask.ext.wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired


class MyView(BaseView):
    @expose('/')
    def ind(self):
        return self.render('index.html')

app = Flask(__name__)
app.config.from_object('config')
admin = Admin(app, name='JAdmin', template_mode='bootstrap3')
db = SQLAlchemy(app)


class RegUser(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))

    def __init__(self, username):
        self.username = username

    def __repr__(self):
        return '<user: %r>' % self.username


class LoginForm(Form):
    username = StringField('username', validators=[DataRequired()])


admin.add_view(ModelView(RegUser, db.session))
admin.add_view(MyView(name='Hello 1', endpoint='test1', category='Test'))
admin.add_view(MyView(name='Hello 2', endpoint='test2', category='Test'))
admin.add_view(MyView(name='Hello 3', endpoint='test3', category='Test'))


@app.route('/login/', methods=['GET', 'POST'])
def hello_world():
    form = LoginForm()
    if form.validate_on_submit():
        new_user = RegUser(form.username.data)
        db.session.add(new_user)
        db.session.commit()
        redirect(url_for('admin.index'))
    return render_template('login.html', form=form)

# db.create_all()
app.run(debug=True)



