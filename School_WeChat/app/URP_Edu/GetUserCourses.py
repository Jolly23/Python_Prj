#!/usr/bin/python
#coding=utf-8

import requests
import string
import json
import re
from bs4 import BeautifulSoup
class GetUserCourses():
    def __init__(self,UserID,Passwd):
        #URLs
        self.Base_URL   = 'http://210.30.7.100:8088/' #'http://zhjw.dlnu.edu.cn/'
        self.Login_URL  = self.Base_URL + 'loginAction.do'
        self.Logout_URL = self.Base_URL + 'logout.do'
        self.GetCourseTable = self.Base_URL + 'xkAction.do?actionType=17'
        self.CourseSearch   = self.Base_URL + 'courseSearchAction.do'
        self.courses_info_url = self.Base_URL + 'courseSearchAction.do'

        #POSTDATAs
        self.Login_PostData = {  'ldap': 'auth',
                            'zjh' : UserID,
                            'mm'  : Passwd    }
        self.Logout_PostData = {'loginType' : 'platformLogin'}

        #HEADERs
        self.headers = {
                    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                    'Accept': 'application/x-www-form-urlencoded',
                    'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
                    'Accept-Encoding':    'gzip, deflate',
                    'Referer':    'http://zhjw.dlnu.edu.cn/gradeLnAllAction.do?type=ln&oper=fa' }
        #SESSIONs
        self.s = requests.Session()

    def GetCourse(self):
        rText = ''
        self.s.get(url=self.Base_URL)
        self.s.post(url=self.Login_URL,data=self.Login_PostData,timeout=5)
        CourseNumbList = []
        req = self.s.get(url=self.GetCourseTable)
        soup = BeautifulSoup(req.text,"lxml")
        courses = soup.find_all('img')
        if courses:
            for course in courses:
                NumbAndOrder = {
                    'CourseNumb' : '',
                    'CourseOrder' : ''
                }
                sign = course.find_next('td').find_next('td').find_next('td')
                if len(sign.string) > 1:
                    course = str(course['name'])
                    courseInfo = re.findall(r'kch=(.*?)&kxh=(\d+)', course)  #using regex find the digit
                    NumbAndOrder['CourseNumb'] = courseInfo[0][0]
                    NumbAndOrder['CourseOrder'] = courseInfo[0][1]
                    CourseNumbList.append(NumbAndOrder)
                    rText = rText + NumbAndOrder['CourseNumb'] + NumbAndOrder['CourseOrder'] + '\n'
        return rText

if __name__ == '__main__':
    aa = GetUserCourses('2013041116','wmild120')
    aa.GetCourse()