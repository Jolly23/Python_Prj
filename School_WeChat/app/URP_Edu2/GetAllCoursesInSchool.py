#!/usr/bin/python
#coding=utf-8

import requests
import sqlite3
import string
import json
import re
from bs4 import BeautifulSoup

class GetAllSchoolCourse():
    def __init__(self):
        #URLs
        self.Base_URL = 'http://210.30.7.100:8088/' #'http://210.30.7.100/'
        self.Login_URL = self.Base_URL + 'loginAction.do'
        self.Logout_URL = self.Base_URL + 'logout.do'
        self.GetCourseTable = self.Base_URL + 'xkAction.do?actionType=17'
        self.CourseSearch = self.Base_URL + 'courseSearchAction.do'
        #POSTDATAs
        self.Login_PostData = {  'ldap': 'auth',
                            'zjh' : '2014131126',#'2013124309',
                            'mm'  : '123456'    }
        self.Logout_PostData = {'loginType' : 'platformLogin'}
        self.SearchPostData = {
                        'pageSize':'200000',
                        'showColumn':[u'kch#课程号'.encode('gbk'),
                                      u'kcm#课程名'.encode('gbk'),
                                      u'kxh#课序号'.encode('gbk'),
                                      u'zcsm#周次'.encode('gbk'),
                                      u'skxq#星期'.encode('gbk'),
                                      u'skjc#节次'.encode('gbk'),
                                      u'xqm#校区'.encode('gbk'),
                                      u'jxlm#教学楼'.encode('gbk'),
                                      u'jasm#教室'.encode('gbk')],
                                        'pageNumber':'0',
                                        'actionType':'1'
                        }
        #HEADERs
        self.headers = {
                    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                    'Accept': 'application/x-www-form-urlencoded',
                    'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
                    'Accept-Encoding':    'gzip, deflate',
                    'Referer':    'http://zhjw.dlnu.edu.cn/gradeLnAllAction.do?type=ln&oper=fa'    }
        #SESSIONs
        self.s = requests.Session()

    def Login(self):
        self.s.get(url=self.Base_URL)
        self.s.post(url=self.Login_URL,data=self.Login_PostData,timeout=5)

    def GetAllCourse(self):
        conn = sqlite3.connect('Courses.db')
        try:
            conn.execute(
            '''
              create table Courses
              (
                C_NUMB    TEXT    NOT NULL ,
                C_NAME    TEXT    NOT NULL ,
                C_ORDER   TEXT    NOT NULL ,
                C_WEEKS   TEXT    NOT NULL ,
                C_DAY     TEXT    NOT NULL ,
                C_TIME    TEXT    NOT NULL ,
                C_PLACE   TEXT    NOT NULL
              );
            '''
            )
            print u'数据库建表成功！'
        except sqlite3.OperationalError:
            print u'数据表已存在，跳过建表'

        self.Login()
        req = self.s.post(url=self.CourseSearch, data=self.SearchPostData,headers=self.headers)
        soup= BeautifulSoup(req.text, 'lxml')
        courses = soup.find_all('tr', class_ = 'odd')

        iii = 0
        for course in courses:
            course_number = course.find('td')
            course_name = course_number.find_next_sibling('td')
            course_order = course_name.find_next_sibling('td')
            weeks = course_order.find_next_sibling('td')
            day = weeks.find_next_sibling('td')
            time = day.find_next_sibling('td')
            school = time.find_next_sibling('td')
            building = school.find_next_sibling('td')
            classroom = building.find_next_sibling('td')
            weeks = weeks.string.strip()
            if len(weeks) > 0:    #skip the  courses which doesen't need go to classroom
                iii = iii + 1
                course_number = course_number.string.strip()
                course_name = course_name.string.strip()
                course_order = course_order.string.strip()
                day = day.string.strip()
                time = time.string.strip()
                all_weeks = []
                week_date = weeks.split(',')
                for date in week_date:
                    week = re.findall(r'\d{1,2}', date, re.X)
                    if u'-' in date:
                        firstWeek = int(week[0])
                        lastWeek = int(week[1])
                        gap = 2
                        if u'单' in weeks:
                            pass
                        elif u'双' in weeks:
                            firstWeek += 1
                        else:
                            gap = 1
                        weeks = [str(week) for week in range(firstWeek,lastWeek+1,gap)]
                    else:
                        weeks = week
                    all_weeks.extend(weeks)
                weeks = json.dumps(all_weeks)
                if u'开发区' in school.string:        #checking which school
                    place = classroom.string.strip()
                else:
                    if building.string == classroom.string:  #skip the same name
                        place = [classroom.string.strip()]
                    else:
                        place = [building.string.strip(),classroom.string.strip()]
                    place = ''.join(place)

                conn.execute("INSERT INTO Courses     \
                             VALUES ('%s','%s','%s','%s','%s','%s','%s')" % (course_number,course_name,course_order,weeks,day,time,place))
                
        conn.commit()
        print u'数据库添加完成，共' + str(iii) + u'个课程'
        conn.close()

if __name__ == '__main__':
    aa = GetAllSchoolCourse()
    aa.GetAllCourse()