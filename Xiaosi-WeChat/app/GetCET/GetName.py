#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-12-16 11:56:32
# @Author  : sxmsr (582124404@qq.com)
# @Link    : www.baidu.com
# @Version : $Id$

import requests
import re
import datetime
from bs4 import BeautifulSoup


class GetName:

    def __init__(self, username, password):
        self.username = username
        self.password = password

        self.proxies = {
            "http": "http://127.0.0.1:8080"
        }

        self.login_url = 'http://zhjw.dlnu.edu.cn/loginAction.do'
        self.get_name_url = "http://zhjw.dlnu.edu.cn/menu/s_top.jsp"

        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                        'Accept': 'application/x-www-form-urlencoded',

                        'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
                        'Accept-Encoding':    'gzip, deflate',
                        'Referer':    'http://zhjw.dlnu.edu.cn/gradeLnAllAction.do?type=ln&oper=fa'
                        }

        self.s = requests.Session()

    def login(self):
        postdata = {
            'zjh': self.username,
            'mm': self.password
        }

        r = self.s.post(
            self.login_url, postdata, headers=self.headers, timeout=2)
        if len(r.text) < 888:
            return True
        else:
            return False

    def get_name(self):
        req = self.s.get(self.get_name_url)
        text = req.text
        items = re.findall(u'欢迎光临&nbsp;(.*?)&nbsp;', text)
        return items[0]

if __name__ == '__main__':
    pe = GetName('', '')
    pe.login()
    pe.get_name()

