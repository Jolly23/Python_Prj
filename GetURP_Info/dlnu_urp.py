# -*- coding: utf-8 -*-
import requests
import string
import json
import re
from bs4 import BeautifulSoup
from urlparse import urljoin
#from settings.config import URP_URL
URP_URL = 'http://210.30.7.100:8088/'

class DlnuUrp(object):
    def __init__(self, stuid, passwd):
        self.login_url = urljoin(URP_URL, 'loginAction.do')
        self.s = requests.Session()

        self.postdata = {
            'ldap': 'auth',
            'zjh': stuid,
            'mm': passwd
            }

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
            'Accept': 'application/x-www-form-urlencoded',
            'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://zhjw.dlnu.edu.cn/gradeLnAllAction.do?type=ln&oper=fa'
            }

    def login(self):
        try:
            req = self.s.get(URP_URL, timeout=(1, 1))
            if req.status_code == 200:
                req = self.s.post(self.login_url, data=self.postdata)
                if u'用户名或密码不正确' in req.text:
                    return 2
                else:
                    return 0
            else:
                return -2

        except requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout:
            return -1
        except requests.exceptions.HTTPError:
            return -2


class GetScore(DlnuUrp):
    def __init__(self, stuid, passwd):
        super(GetScore, self).__init__(stuid, passwd)
        self.all_score_url = urljoin(URP_URL, 'gradeLnAllAction.do?type=ln&oper=fa')
        self.recent_score_url = urljoin(URP_URL, 'bxqcjcxAction.do')
        self.resit_score_url = urljoin(URP_URL, 'cjSearchAction.do?oper=getKscjList')

    def get_all_score(self):
        req = self.s.get(self.all_score_url)
        soup = BeautifulSoup(req.text, "lxml")
        tag = soup.find('iframe')
        req = self.s.get(URP_URL+tag['src'])
        soup = BeautifulSoup(req.text, "lxml")
        all_exams = soup.find_all('tr', class_='odd')

        exam_list = []
        for exam in all_exams:
            course_num = exam.find('td')
            course_order = course_num.find_next('td')
            course_name = course_order.find_next('td')
            course_credit = course_name.find_next('td').find_next('td')
            course_score = course_credit.find_next('td').find_next('td')

            try:
                c_order = int(string.strip(course_order.text))
            except ValueError:
                c_order = 0
            exam_info = {
                'course_num': string.strip(course_num.text),
                'course_order': c_order,
                'course_name': string.strip(course_name.text),
                'course_credit': float(string.strip(course_credit.text)),
                'course_score': string.strip(course_score.text),
                }
            exam_list.append(exam_info)
        return exam_list

    def get_recent_score(self):
        req = self.s.get(self.recent_score_url)
        soup = BeautifulSoup(req.text, "lxml")
        recent_exams = soup.find_all('tr', class_='odd')
        exam_list = []

        for exam in recent_exams:
            course_num = exam.find_next('td')
            course_order = course_num.find_next('td')
            course_name = course_order.find_next('td')
            course_credit = course_name.find_next('td').find_next('td')
            course_score = course_credit.find_next('td').find_next('td')

            exam_info = {
                'course_num': string.strip(course_num.text),
                'course_order': int(string.strip(course_order.text)),
                'course_name': string.strip(course_name.text),
                'course_credit': float(string.strip(course_credit.text)),
                'course_score': string.strip(course_score.text),
                }
            exam_list.append(exam_info)
        return exam_list

    def get_resit_score(self):
        req = self.s.get(self.resit_score_url)
        soup = BeautifulSoup(req.text, "lxml")
        recent_exam = soup.find_all('tr', class_='odd')
        exam_list = []

        for exam in recent_exam:
            course_num = exam.find_next('td')
            course_order = course_num.find_next('td')
            course_name = course_order.find_next('td')
            course_credit = course_name.find_next('td').find_next('td')
            course_score = course_credit.find_next('td')

            exam_info = {
                'course_num': string.strip(course_num.text),
                'course_order': int(string.strip(course_order.text)),
                'course_name': string.strip(course_name.text),
                'course_credit': float(string.strip(course_credit.text)),
                'course_score': string.strip(course_score.text),
                }
            exam_list.append(exam_info)
        return exam_list


class GetCourses(DlnuUrp):
    def __init__(self, stuid, passwd):
        super(GetCourses, self).__init__(stuid, passwd)
        self.get_course_table_url = urljoin(URP_URL, 'xkAction.do?actionType=17')
        self.course_search_url = urljoin(URP_URL, 'courseSearchAction.do')

    def get_courses(self):
        req = self.s.get(self.get_course_table_url)
        soup = BeautifulSoup(req.text, "lxml")
        courses = soup.find_all('img')
        user_course_list = []
        if courses:
            for course in courses:
                sign = string.strip(course.find_next('td').find_next('td').find_next('td').text)
                if sign:
                    course = str(course['name'])
                    course_key = re.findall(r'kch=(.*?)&kxh=(\d+)', course)
                    course_info = {
                        'course_num': course_key[0][0],
                        'course_order': int(course_key[0][1]),
                        }
                    user_course_list.append(course_info)
        return user_course_list

    def all_school_courses(self):
        post_data = {
            'pageSize': '200000',
            'showColumn': [
                u'kch#课程号'.encode('gbk'),
                u'kcm#课程名'.encode('gbk'),
                u'kxh#课序号'.encode('gbk'),
                u'zcsm#周次'.encode('gbk'),
                u'skxq#星期'.encode('gbk'),
                u'skjc#节次'.encode('gbk'),
                u'xqm#校区'.encode('gbk'),
                u'jxlm#教学楼'.encode('gbk'),
                u'jasm#教室'.encode('gbk')],
            'pageNumber': '0',
            'actionType': '1',
            }
        req = self.s.post(self.course_search_url, data=post_data, headers=self.headers)
        soup = BeautifulSoup(req.text, "lxml")
        courses = soup.find_all('tr', class_='odd')
        course_list = []

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
            if weeks:    # skip the  courses which doesn't need go to classroom
                all_weeks = []
                week_date = weeks.split(',')
                for date in week_date:
                    week = re.findall(r'\d{1,2}', date, re.X)
                    if u'-' in date:
                        first_week = int(week[0])
                        last_week = int(week[1])
                        gap = 2
                        if u'单' in weeks:
                            pass
                        elif u'双' in weeks:
                            first_week += 1
                        else:
                            gap = 1
                        weeks = [str(week) for week in range(first_week, last_week+1, gap)]
                    else:
                        weeks = week
                    all_weeks.extend(weeks)
                weeks = json.dumps(all_weeks)
                if u'开发区' in school.string:
                    place = classroom.string.strip()
                else:
                    if building.string == classroom.string:
                        place = [classroom.string.strip()]
                    else:
                        place = [building.string.strip(), classroom.string.strip()]
                    place = ''.join(place)
                course_info = {
                    'course_num': course_number.string.strip(),
                    'course_name': course_name.string.strip(),
                    'course_order': int(course_order.string.strip()),
                    'course_weeks': weeks,
                    'course_day': int(day.string.strip()),
                    'course_time': int(time.string.strip()),
                    'course_place': place,
                    }
                course_list.append(course_info)
        return course_list

if __name__ == '__main__':
    '''
    a = GetScore('2014131201', '123456')
    a.login()
    xxx = a.get_all_score()
    for ii in xxx:
        if ii['course_num'] == '09200001':
            print ii['course_name'], ii['course_order']

    print a.get_recent_score()
    print a.get_resit_score()
    '''
    b = GetCourses('2014131126', '123456')
    b.login()
    bb = b.get_courses()
    print bb
    bb = b.all_school_courses()
    for ii in bb:
        if u'高等数学' in ii['course_name']:
            print ii['course_name'], ii['course_order']


if __name__ == '__main__':
    a = GetCourses('2014131126', '123456')
    a.login()
    print a.get_courses()
