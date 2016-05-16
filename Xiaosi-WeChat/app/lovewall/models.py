#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-12-05 16:01:31
# @Author  : sxmsr (582124404@qq.com)
# @Link    : www.baidu.com
# @Version : $Id$

from datetime import datetime
from app import db


class LoveWall(db.Model):
    __tablename__ = "love_wall"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer)
