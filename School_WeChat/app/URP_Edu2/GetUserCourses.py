#!/usr/bin/python
#coding=utf-8

import requests
import sqlite3
import string
import json
import re
import os
import datetime
from bs4 import BeautifulSoup

class GetUserCourses():
    def __init__(self, userid, passwd):
        #URLs
        self.base_url   = 'http://210.30.7.100:8088/' #'http://zhjw.dlnu.edu.cn/'
        self.login_url  = self.base_url + 'loginAction.do'
        self.logout_url = self.base_url + 'logout.do'
        self.get_course_table_url = self.base_url + 'xkAction.do?actionType=17'
        self.course_search_url = self.base_url + 'courseSearchAction.do'
        self.courses_info_url = self.base_url + 'courseSearchAction.do'
        self.get_week_url = 'http://210.30.7.100:8089/mhpd/xl.jsp'

        #POSTDATAs
        self.login_postdata = {  'ldap': 'auth',
                            'zjh' : userid,
                            'mm'  : passwd    }

        #HEADERs
        self.headers = {
                    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                    'Accept': 'application/x-www-form-urlencoded',
                    'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
                    'Accept-Encoding':    'gzip, deflate',
                    'Referer':    'http://zhjw.dlnu.edu.cn/gradeLnAllAction.do?type=ln&oper=fa' }
        #SESSIONs
        self.s = requests.Session()

    def getcourse(self):
        dbpath = os.path.abspath(os.path.dirname(__file__))
        conn = sqlite3.connect(dbpath + '/Courses.db')
        rtext = ''
        self.s.get(url=self.base_url)
        self.s.post(url=self.login_url,data=self.login_postdata,timeout=5)
        req = self.s.get(url=self.get_course_table_url)
        soup = BeautifulSoup(req.text,"lxml")
        courses = soup.find_all('img')
        if courses:
            for course in courses:
                sign = course.find_next('td').find_next('td').find_next('td')
                if len(sign.string) > 1:
                    course = str(course['name'])
                    courseInfo = re.findall(r'kch=(.*?)&kxh=(\d+)', course)
                    cursor = conn.execute("SELECT * FROM Courses WHERE C_NUMB='%s' AND C_ORDER='%s';" % (courseInfo[0][0],courseInfo[0][1]))
                    for xx in cursor:
                        rtext = rtext + xx[1] + '\n'
        conn.close()
        return rtext

    def getnowcourse(self):
        weekday = datetime.date.today().weekday()   # 0 == Monday
        print weekday

    def get_week(self):
        req = self.s.get(url=self.get_week_url)
        print req.text
        sooo = BeautifulSoup(req.text, "lxml")
        rr = sooo.find('font', size="6", color="#976147")   #周数
        print rr.text

if __name__ == '__main__':
    aa = GetUserCourses('2014131126','123456')
    aa.get_week()