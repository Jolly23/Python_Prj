#!/usr/bin/python
#coding=utf-8

import requests
import string
from bs4 import BeautifulSoup

class URP_GetScore():
    def __init__(self,UserID,Passwd):
        #URLs
        self.Base_URL   = 'http://210.30.7.100:8088/' #'http://zhjw.dlnu.edu.cn/'
        self.Login_URL  = self.Base_URL + 'loginAction.do'
        self.GetCode_URL    = self.Base_URL + 'gradeLnAllAction.do?type=ln&oper=fa'
        self.GetScore_URL   = self.Base_URL + 'gradeLnAllAction.do?type=ln&oper=fainfo&fajhh='
        self.Logout_URL     = self.Base_URL + 'logout.do'
        self.GetRecentScore_URL = self.Base_URL + 'bxqcjcxAction.do'
        self.GetResitScore_URL  = self.Base_URL + 'cjSearchAction.do?oper=getKscjList'

        #SESSIONs
        self.s = requests.Session()

        #POSTDATAs
        self.Login_PostData = {
                    'ldap': 'auth',
                    'zjh' : UserID,
                    'mm'  : Passwd   }

        self.Logout_PostData = {'loginType' : 'platformLogin'}

        #HEADERs
        self.headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
            'Accept': 'application/x-www-form-urlencoded',
            'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
            'Accept-Encoding':    'gzip, deflate',
            'Referer':    'http://zhjw.dlnu.edu.cn/gradeLnAllAction.do?type=ln&oper=fa' }

    def login(self):
        self.s.get(url=self.Base_URL)
        LSreq = self.s.post(url=self.Login_URL,data=self.Login_PostData,timeout=5)
        if u'用户名或密码不正确' in LSreq.text:
            return False
        else:
            return True

    def AccountCheck(self):
        return self.login()

    def logout(self):
        self.s.post(url=self.Logout_URL,data=self.Logout_PostData,timeout=5)

    def GetAllScore(self):
        if self.login():
            LSreq   = self.s.get(url=self.GetCode_URL,headers=self.headers,timeout=5)
            soup    = BeautifulSoup(LSreq.text,"html.parser")
            tag     = soup.find('iframe')
            LSreq   = self.s.get(url=self.Base_URL + tag['src'],timeout=5)
            soup    = BeautifulSoup(LSreq.text,"html.parser")
            AllExams = soup.find_all('tr',class_ = 'odd')

            AllExamInfoList = []
            for exam in AllExams:
                ExamInfo = {
                    'COURSE_NUMB'   :'',
                    'COURSE_ORDER'  :'',
                    'COUSER_NAME'   :'',
                    'COURSE_CREDIT' :'',
                    'COURSE_SCORE'  :'',
                }
                course_num      = exam.find('td')
                course_order    = course_num.find_next('td')
                course_name     = course_order.find_next('td')
                course_credit   = course_name.find_next('td').find_next('td')
                course_score    = course_credit.find_next('td').find_next('td')

                ExamInfo['COURSE_NUMB']     = string.strip(course_num.text)
                ExamInfo['COURSE_ORDER']    = string.strip(course_order.text)
                ExamInfo['COUSER_NAME']     = string.strip(course_name.text)
                ExamInfo['COURSE_CREDIT']   = string.strip(course_credit.text)
                ExamInfo['COURSE_SCORE']    = string.strip(course_score.text)
                AllExamInfoList.append(ExamInfo)
            return AllExamInfoList  #-----------------------------------------------------------
            self.logout()
            return True
        else:
            return False


    def GetRecentScore(self):
        if self.login():
            LSreq   = self.s.get(url=self.GetRecentScore_URL,timeout=5)
            soup    = BeautifulSoup(LSreq.text,"html.parser")
            RecentExams = soup.find_all('tr',class_ = 'odd')
            RecentExamInfoList = []

            for exam in RecentExams:
                ExamInfo = {
                    'COURSE_NUMB'   :'',
                    'COURSE_ORDER'  :'',
                    'COUSER_NAME'   :'',
                    'COURSE_CREDIT' :'',
                    'COURSE_SCORE'  :'',
                }
                course_num      = exam.find_next('td')
                course_order    = course_num.find_next('td')
                course_name     = course_order.find_next('td')
                course_credit   = course_name.find_next('td').find_next('td')
                course_score    = course_credit.find_next('td').find_next('td')

                ExamInfo['COURSE_NUMB']     = string.strip(course_num.text)
                ExamInfo['COURSE_ORDER']    = string.strip(course_order.text)
                ExamInfo['COUSER_NAME']     = string.strip(course_name.text)
                ExamInfo['COURSE_CREDIT']   = string.strip(course_credit.text)
                ExamInfo['COURSE_SCORE']    = string.strip(course_score.text)
                RecentExamInfoList.append(ExamInfo)
            return RecentExamInfoList  #-----------------------------------------------------------
            self.logout()
        else:
            return False

    def GetResitScore(self):
        if self.login():
            LSreq   = self.s.get(url=self.GetResitScore_URL,timeout=5)
            soup    = BeautifulSoup(LSreq.text,"html.parser")
            RecentExams = soup.find_all('tr',class_ = 'odd')
            ResitExamInfoList = []

            for exam in RecentExams:
                ExamInfo = {
                    'COURSE_NUMB'   :'',
                    'COURSE_ORDER'  :'',
                    'COUSER_NAME'   :'',
                    'COURSE_CREDIT' :'',
                    'COURSE_SCORE'  :'',
                }
                course_num      = exam.find_next('td')
                course_order    = course_num.find_next('td')
                course_name     = course_order.find_next('td')
                course_credit   = course_name.find_next('td').find_next('td')
                course_score    = course_credit.find_next('td')

                ExamInfo['COURSE_NUMB']     = string.strip(course_num.text)
                ExamInfo['COURSE_ORDER']    = string.strip(course_order.text)
                ExamInfo['COUSER_NAME']     = string.strip(course_name.text)
                ExamInfo['COURSE_CREDIT']   = string.strip(course_credit.text)
                ExamInfo['COURSE_SCORE']    = string.strip(course_score.text)
                ResitExamInfoList.append(ExamInfo)
            self.logout()
        else:
            print u'密码错误'

if __name__ == '__main__':
    USER = URP_GetScore('2014131126','123456')
    USER.GetRecentScore()
    USER.GetAllScore()
