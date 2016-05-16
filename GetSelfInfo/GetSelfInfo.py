#!/usr/bin/python
# coding=utf-8

import requests
import string
from bs4 import BeautifulSoup


class GetStuInfo():
    def __init__(self, stuid, passwd):
        self.stuid = stuid
        self.base_url = 'http://210.30.7.100:8088/'
        self.login_url = self.base_url + 'loginAction.do'
        self.basicinfo_url = self.base_url + 'userInfo.jsp'
        self.detailinfo_url = self.base_url + 'xjInfoAction.do?oper=xjxx'

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
            self.s.get(url=self.base_url)
            req = self.s.post(url=self.login_url, data=self.postdata, headers=self.headers)
            if req.status_code == 200:
                if u'密码不正确' in req.text:
                    return 2
                else:
                    return 0
            else:
                return -2

        except requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout:
            return -1
        except requests.exceptions.HTTPError:
            return -2

    def get_basicinfo(self):
        basicdata = {
            'name': '',             # 姓名
            'stuid': self.stuid,    # 学号
            'phone': '',            # 电话
            'email': '',            # 邮件地址
        }
        req = self.s.get(url=self.basicinfo_url)
        soup = BeautifulSoup(req.text, "lxml")
        name_tag = soup.find('td', width="215", align="right", class_="fieldName").find_next().text
        basicdata['name'] = string.strip(name_tag)
        infos = soup.find_all(type="text")
        basicdata['phone'] = infos[0]['value']
        basicdata['email'] = infos[2]['value']
        return basicdata

    def get_detailinfo(self):
        basicdata = self.get_basicinfo()
        detaildata = {
            'name': basicdata['name'],  # 姓名
            'en_name': '',              # 英文姓名
            'id_card_no': '',           # 身份证号
            'gender': '',               # 性别
            'stuid': basicdata['stuid'],        # 学号
            'phone': basicdata['phone'],        # 电话
            'email': basicdata['email'],        # 电子邮件地址
            'nationality': '',          # 民族
            'province': '',             # 籍贯
            'middle_school': '',        # 毕业中学
            'gk_score': '',             # 高考分数
            'department': '',           # 所属院系
            'major': '',                # 专业
            'class': '',                # 班级
            'campus': '',               # 校区
            }

        req = self.s.get(url=self.detailinfo_url)
        soup = BeautifulSoup(req.text, "lxml")
        tags = soup.find_all('td', class_="fieldName", width="180")

        en_name_tag = tags[3].find_next()
        detaildata['en_name'] = string.strip(en_name_tag.text)

        id_card_no_tag = tags[5].find_next()
        detaildata['id_card_no'] = string.strip(id_card_no_tag.text)

        gender_tag = tags[6].find_next()
        detaildata['gender'] = string.strip(gender_tag.text)

        nationality_tag = tags[11].find_next()
        detaildata['nationality'] = string.strip(nationality_tag.text)

        province_tag = tags[15].find_next()
        detaildata['province'] = string.strip(province_tag.text)

        middle_school_tag = tags[16].find_next()
        detaildata['middle_school'] = string.strip(middle_school_tag.text)

        gk_score_tag = tags[17].find_next()
        detaildata['gk_score'] = string.strip(gk_score_tag.text)

        department_tag = tags[25].find_next()
        detaildata['department'] = string.strip(department_tag.text)

        major_tag = tags[26].find_next()
        detaildata['major'] = string.strip(major_tag.text)

        class_tag = tags[29].find_next()
        detaildata['class'] = string.strip(class_tag.text)

        campus_tag = tags[32].find_next()
        detaildata['campus'] = string.strip(campus_tag.text)

        return detaildata


if __name__ == "__main__":
    aa = GetStuInfo('2014131205', '941007')
    aa.login()
    ret = aa.get_detailinfo()
    print ret
    for k, v in ret.items():
        print k, v