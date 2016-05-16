#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-12-05 16:58:34
# @Author  : sxmsr (582124404@qq.com)
# @Link    : www.baidu.com
# @Version : $Id$

from flask.ext.wtf import Form
from wtforms import SubmitField, TextAreaField
from wtforms.validators import Required


class LoveForm(Form):
    body = TextAreaField("What's on your mind?", validators=[Required()])
    submit = SubmitField('wall run')
