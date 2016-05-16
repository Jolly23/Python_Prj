#!/usr/bin?python
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
URP_URL = 'http://210.30.1.60/'
# 'http://zhjw.dlnu.edu.cn/'    # 'http://210.30.7.100:8088/'


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
            req = self.s.get(URP_URL)
            if req.status_code == 200:
                req = self.s.post(self.login_url, data=self.postdata)
                if u'用户名或密码不正确' in req.text:
                    return 2
                else:
                    return 0
            else:
                return -2
        except:
            return -1


class GetStuInfo(DlnuUrp):
    def __init__(self, stuid, passwd):
        self.stuid = stuid
        super(GetStuInfo, self).__init__(stuid, passwd)
        self.basicinfo_url = urljoin(URP_URL, 'userInfo.jsp')
        self.detailinfo_url = urljoin(URP_URL, 'xjInfoAction.do?oper=xjxx')

    def get_basic_info(self):
        req = self.s.get(self.basicinfo_url)
        soup = BeautifulSoup(req.text, "lxml")
        name_tag = soup.find('td', width="215", align="right", class_="fieldName").find_next()
        infos = soup.find_all(type="text")
        return {
            'name': name_tag.string.strip(),  # 姓名
            'stuid': self.stuid,              # 学号
            'phone': infos[0]['value'],       # 电话
            'email': infos[2]['value'],       # 邮件地址
        }

    def get_detail_info(self):
        req = self.s.get(self.detailinfo_url)
        soup = BeautifulSoup(req.text, "lxml")
        tags = soup.find_all('td', class_="fieldName", width="180")
        gender_tag = tags[6].find_next()
        department_tag = tags[25].find_next()
        major_tag = tags[26].find_next()
        class_tag = tags[29].find_next()
        basicdata = self.get_basic_info()

        return {
            'name': basicdata['name'],                          # 姓名
            'gender': gender_tag.string.strip(),                # 性别
            'stuid': basicdata['stuid'],                        # 学号
            'phone': basicdata['phone'],                        # 电话
            'email': basicdata['email'],                        # 电子邮件地址
            'department': department_tag.string.strip(),        # 所属院系
            'major': major_tag.string.strip(),                  # 专业
            'class': class_tag.string.strip(),                  # 班级
        }


if __name__ == '__main__':
    majors = (u'软件工程', u'网络工程', u'计算机科学与技术', u'电子信息工程', u'通信工程', u'物联网工程',
              u'信息与计算科学', u'信息与计算科学', u'自动化', u'测控技术与仪器', u'机械设计制造及其自动化',
              u'工业工程', u'产品设计')

    # qInfo = Queue()

    def get_info(user):
        fun = GetStuInfo(user[0], user[1])
        if fun.login() == 0:
            info = fun.get_detail_info()
            if info['major'] in majors and len(info['phone']) == 11:
                print info['name'], '\t', info['major'], '\t', info['phone']
                # qInfo.put_nowait({'name': info['name'], 'major': info['major'], 'phone': info['phone']})

    conn = sqlite3.connect('User.db')
    # db_msg = conn.execute("SELECT * FROM USERS WHERE UID GLOB '2013*';")
    db_msg = conn.execute("SELECT * FROM USERS WHERE UID LIKE '2013%';")

    users = []
    for msg in db_msg:
        users.append(msg)
    print len(users)

    pool = Pool(64)
    start = time.time()

    pool.map(get_info, users)

    pool.close()
    pool.join()

    print u'用时', time.time() - start, u'秒'
    # print qInfo.qsize()

    '''

def __format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(
        (
            Header(name, 'utf-8').encode(), addr.encode('utf-8') if isinstance(addr, unicode) else addr
        )
    )


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