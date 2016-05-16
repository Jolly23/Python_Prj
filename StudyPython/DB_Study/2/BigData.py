# -*- coding: utf-8 -*-
import requests
import string
import sqlite3
import time
from email.mime.text import MIMEText
from email import encoders
from email.header import Header
from email.utils import parseaddr, formataddr
import smtplib
from bs4 import BeautifulSoup
from urlparse import urljoin
from multiprocessing import Queue, Pool

URP_URL = 'http://210.30.7.100:8088/'

class DlnuUrp(object):
    def __init__(self, stuid, passwd):
        self.login_url = urljoin(URP_URL, 'loginAction.do')
        self.all_score_url = urljoin(URP_URL, 'gradeLnAllAction.do?type=ln&oper=fa')
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
        except :
            return -1

class GetScore(DlnuUrp):
    def get_all_score(self):
        req = self.s.get(self.all_score_url)
        soup = BeautifulSoup(req.text, "lxml")
        tag = soup.find('iframe')
        req = self.s.get(URP_URL+tag['src'])
        soup = BeautifulSoup(req.text, "lxml")
        all_exams = soup.find_all('tr', class_='odd')

        exam_list = []
        for exam in all_exams:
            course_name = exam.find('td').find_next('td').find_next('td')
            course_score = course_name.find_next('td').find_next('td').find_next('td').find_next('td')
            exam_info = {
                'course_name': string.strip(course_name.text),
                'course_score': string.strip(course_score.text),
                }
            exam_list.append(exam_info)
        return exam_list


def __format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(
        (
            Header(name, 'utf-8').encode(), addr.encode('utf-8') if isinstance(addr, unicode) else addr
        )
    )

if __name__ == '__main__':
    qScore = Queue()
    qPwdErr = Queue()

    def get_math(user):
        fun = GetScore(user[0], user[1])
        if fun.login() == 0:
            global qScore
            ret = fun.get_all_score()
            for x in ret:
                if u'数学' in x['course_name']:
                    print x['course_name'],
                    try:
                        s = float(x['course_score'])
                        print s
                        qScore.put(s)
                    except ValueError:
                        continue
        else:
            qPwdErr.put(1)
        print 'done'

    def get_error_pw(user):
        fun = GetScore(user[0], user[1])
        if fun.login() == 2:
            qPwdErr.put(user[0])
            print user[0]

    conn = sqlite3.connect('User.db')
    l = conn.execute("SELECT * FROM USERS LIMIT 10;")
    ll = []

    for i in l:
        ll.append(i)

    pool = Pool(16)
    a = time.time()

    pool.map(get_error_pw, ll)

    pool.close()
    pool.join()

    #err_count = 0
    #while qPwdErr.empty() is False:
    #    err_count += 1

    print u'Err数', qPwdErr.qsize()
    print u'用时', time.time() - a, u'秒'

    result_text = u'总账户数：%d \n' % len(ll)
    result_text = result_text + u'密码失效账户数: %d \n' % qPwdErr.qsize()
    while qPwdErr.empty() is False:
        result_text = result_text + str(qPwdErr.get()) + '\n'
    result_text = result_text + u'共用时 %s秒 \n' % str(time.time() - a)

    print result_text
    '''
    from_addr = '903221074@qq.com'
    passwd = 'Aston77Martin'
    SMTP_Server = 'smtp.qq.com'
    Sendto = '903221074@qq.com'

    msg = MIMEText(result_text, 'plain', 'utf-8')
    msg['From'] = __format_addr(u'Jolly_Python<%s>' % from_addr)
    msg['To'] = __format_addr(u'管理员<%s>' % Sendto)
    msg['Subject'] = Header(u'试验结果  --来自赵磊的Python', 'utf-8').encode()

    server = smtplib.SMTP(SMTP_Server, 25)
    server.set_debuglevel(1)
    server.login(from_addr, passwd)
    server.sendmail(from_addr, [Sendto], msg.as_string())

    server.quit()
    '''