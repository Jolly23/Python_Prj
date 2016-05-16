#!/usr/bin/python
#coding=utf-8

import requests
from bs4 import BeautifulSoup
import re
import hashlib
import json
import time

Base_URL    = 'http://210.30.7.100:8090/Self/'
Login_URL   = Base_URL + 'LoginAction.action'
Random_URL  = Base_URL + 'RandomCodeAction.action'
GetFlow_URL = Base_URL + 'nav_getUserInfo'
MainPage_URL= Base_URL + 'nav_main'
AcStatus_URL= Base_URL + 'refreshaccount?t=0.521180426934734'
Overdate_URL= Base_URL + 'MonthPayAction.action'

getlogoutsessionid_url = Base_URL + 'nav_offLine'
logout_url = Base_URL + 'tooffline'


class Drcom():
    def __init__(self, username, password):
        self.s = requests.Session()
        self.Username = username
        self.Password = hashlib.md5(password).hexdigest()
        self.Send_Headers = {
                    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:14.0) Gecko/20100101 Firefox/14.0.1',
                    'Accept': 'application/x-www-form-urlencoded',
                    'Accept-Language': 'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
                    'Accept-Encoding':    'gzip, deflate',
                    'Referer':    'http://zhjw.dlnu.edu.cn/gradeLnAllAction.do?type=ln&oper=fa'
        }

    def login(self):
        req = self.s.get(Login_URL, timeout = 5)
        self.s.get(Random_URL)
        checkcode = re.findall('var checkcode="(\d*)', req.text, re.S)
        self.postdata = {'account': self.Username,
                'password':self.Password,
                'code':'',
                'checkcode':checkcode[0],
                'Submit':'%E7%99%BB+%E5%BD%95'
        }
        sRes = self.s.post(url=Login_URL,data=self.postdata,timeout=5)
        if u'温馨提示' in sRes.text:
            return True
        else:
            return False

    def AccountCheck(self):
        return self.login()

    def GetFlow(self):
        req = self.s.get(GetFlow_URL)
        text = req.text
        soup = BeautifulSoup(text, "lxml")
        tag = soup.find('td', text = re.compile(u"本月流量"))
        tag = tag.find_next_sibling('td')
        sRes = re.findall('(\d+).\d',tag.string)
        self.AcFlowUsed = float(sRes[0]) / 1000.0  #转换单位M->G

    def GetAcStatus(self):
        req = self.s.get(AcStatus_URL)
        GetData = json.loads(req.text)
        AcStatus = GetData['note']
        self.AcUsername     =   AcStatus['welcome']
        self.AcLeftMoeny    =   AcStatus['leftmoeny']
        self.AcService      =   AcStatus['service']
        self.AcOnlineStatus =   AcStatus['onlinestate']
        sGetFlowLimit = re.findall('(\d+)G',AcStatus['service'])      #提取套餐流量限制
        self.AcFlowLimit = float(sGetFlowLimit[0])

    def GetOverData(self):
        req = self.s.post(Overdate_URL, data = {'type': '1' ,'year': time.gmtime()[0]})
        soup = BeautifulSoup(req.text, "lxml")
        try:
            soup = soup.find('tbody').find('td').find_next_sibling('td')
            self.AcOverDate = str(soup.string)
        except AttributeError:  # if the date was Null
            self.AcOverDate = u'不详'
    
    def RetDrcomInfo(self):
        RetText = ''
        if self.login():
            self.GetFlow()
            self.GetAcStatus()
            self.GetOverData()
            RetText = self.AcUsername + '\n'
            if self.AcOnlineStatus == u'1':
                RetText = RetText + u"----!-在线-!----" + '\n'
            else:
                RetText = RetText + u"----x-离线-x----" + '\n'
            RetText = RetText + u"已用流量：" + str(self.AcFlowUsed) + "G" + '\n'
            #print u"套餐总流量：",self.AcFlowLimit
            RetText = RetText + u"剩余流量：" + str(self.AcFlowLimit - self.AcFlowUsed) + "G" + '\n'
            RetText = RetText + u"到期时间：" + self.AcOverDate + '\n'
            RetText = RetText + u"账户余额：" + self.AcLeftMoeny

        else:
            RetText = u'校园网密码错误，请重新绑定！'

        return RetText
    
    def PrintStatus(self):
        print "************************"
        print self.AcUsername,
        if self.AcOnlineStatus == u'1':
            print u"!-在线-!"
        else:
            print u"--离线--"
        print u"已用流量：",self.AcFlowUsed,"G"
        #print u"套餐总流量：",self.AcFlowLimit
        print u"剩余流量：  ",self.AcFlowLimit - self.AcFlowUsed,"G"
        print u"到期时间：  ",self.AcOverDate
        print self.AcService
        print u"账户余额：",self.AcLeftMoeny
        print "************************",'\n'

    def logout(self):
        RetText = ''
        if self.login():
            req = self.s.get(url=getlogoutsessionid_url)
            ssoup = BeautifulSoup(req.text,"lxml")
            tags = ssoup.find_all('td', style = 'display:none;')
            for tag in tags:
                sessionid = tag.string
                self.s.get(logout_url, params = {'t': '', 'fldsessionid': sessionid})
            RetText = u'Success!' + str(len(tags))
        else:
            RetText = u'校园网密码错误，请重新绑定！'

        return RetText    


if __name__ == '__main__':
    aa = Drcom('2014131126','Chanel-5')
    if aa.login():
        aa.GetFlow()
        aa.GetAcStatus()
        aa.GetOverData()
        aa.PrintStatus()

    else:
        print u"PassWord Error!"
