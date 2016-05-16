#coding=utf-8
from flask import render_template, flash, redirect, url_for
from app import app, db
from .forms import LoginForm
from .models import regUser


@app.route('/bind/<string:openid>', methods=['GET', 'POST'])
def bind(openid=None):
    openid = openid
    form = LoginForm()
    if form.validate_on_submit() and openid:
        #user = regUser(openid, form.username.data, form.password_urp.data, form.password_drcom.data)
        #db.session.add(user)
        #db.session.commit()
        return render_template('succeed.html')

    return render_template('login.html',
                           title='Sign In',
                           form=form)


@app.route('/')
def a():
    openid = '123'
    return url_for('bind', openid=openid)
