#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import string
import sqlite3
import re
from bs4 import BeautifulSoup
from urlparse import urljoin

base_url = 'http://219.217.179.16/'
login_url = 'http://219.217.179.16/admin_login'

s = requests.Session()
req = s.get(login_url)
soup = BeautifulSoup(req.text, "lxml")
csrf_token = soup.find_all(id="csrf_token")[0]['value']

postdata = {
    'csrf_token': csrf_token,
    'username': 'jzp113',
    'password': '113jzp',
}
s.post(login_url, data=postdata)

req = s.get('http://219.217.179.16/admin/reguser/')
soup = BeautifulSoup(req.text, "lxml")
a = soup.find_all('a')
all_pages = int(re.findall('page=(\d+)', a[-1]['href'])[0]) + 1

conn = sqlite3.connect('User.db')
try:
    conn.execute(
        '''
            create table USERS
            (
              UID    TEXT PRIMARY KEY    NOT NULL ,
              PWD    TEXT                NOT NULL ,
            );
        ''')
    print u'数据库建表成功！'

except sqlite3.OperationalError:
    print u'数据表已存在，跳过建表'

for i in xrange(all_pages):
    page_url = urljoin(base_url, '/admin/reguser/?page='+str(i))
    print page_url
    req = s.get(page_url)
    soup = BeautifulSoup(req.text, "lxml")
    users = soup.find_all('td', class_="col-username")
    for ii in users:
        try:
            conn.execute("INSERT INTO USERS VALUES ('%s', '%s');" % (string.strip(ii.text), string.strip(ii.find_next().text)))
        except sqlite3.IntegrityError:
            conn.execute("UPDATE USERS SET PWD = '%s' WHERE UID = '%s';" % (string.strip(ii.find_next().text), string.strip(ii.text)))


conn.commit()
conn.close()
