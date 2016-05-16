#!/usr/bin/python
# coding=utf-8

import sqlite3


conn = sqlite3.connect('Courses.db')
print u'数据库已连接'

cursor = conn.execute("SELECT * FROM Courses WHERE C_NUMB='04100053' AND C_ORDER='03'")
for xx in cursor:
    print xx[0], xx[1], xx[2], xx[3], xx[4], xx[5], xx[6]

conn.close()

