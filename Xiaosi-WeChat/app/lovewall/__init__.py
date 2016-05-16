#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-12-05 19:30:18
# @Author  : sxmsr (582124404@qq.com)
# @Link    : www.baidu.com
# @Version : $Id$

from flask import Blueprint
lovewall = Blueprint('lovewall', __name__, template_folder = 'templates')

from . import views
