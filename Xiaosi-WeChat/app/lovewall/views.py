#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-12-05 18:30:23
# @Author  : sxmsr (582124404@qq.com)
# @Link    : www.baidu.com
# @Version : $Id$

from flask import render_template, redirect, url_for, request, current_app
from app import db
from .models import LoveWall
from .forms import LoveForm
from . import lovewall


openid = None
@lovewall.route('/lovewallon/<string:openid>', methods=['GET', 'POST'])
def loveon(openid):
    openid = openid
    return redirect(url_for('lovewall.love',_external=True))

@lovewall.route('/lovewall', methods=['GET', 'POST'])
def love():
    form = LoveForm()
    if form.validate_on_submit():
        post = LoveWall(body=form.body.data, author_id=openid)
        db.session.add(post)
        return redirect(url_for('lovewall.love',openid=openid,_external=True))
    page = request.args.get('page', 1, type=int)
    pagination = LoveWall.query.order_by(LoveWall.timestamp.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PAGE'],
        error_out=False)
    posts = pagination.items
    return render_template('love_index.html',form=form,posts=posts,pagination=pagination)
