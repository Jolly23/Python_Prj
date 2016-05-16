#!/usr/bin/python
# coding=utf-8

import re
import requests


class DrChPsw:
    def __init__(self, stuid, oldPass, newPass):
        self.chpasswd_url = 'http://172.16.192.111/a29.htm'
        self.postdata = {
            'DDDDD': stuid,
            'upass': oldPass,
            'npass': newPass,
            'Npass': newPass,
            '3MKKey': ''
        }
        self.s = requests.Session()

    def chpasswd(self):
        req = self.s.post(url=self.chpasswd_url, data=self.postdata)
        ss = re.findall('Msg=(\d+)', req.text)
        print ss[0]

        '''
        01:账号或密码不对，请重新输入
        10:密码修改成功
        4:本账号费用超支或时长流量超过限制
        5:本账号暂停使用
        8:本账号正在使用,不能修改

        9:新密码与确认新密码不匹配,不能修改 (提交时就被禁止)
        '''


if __name__ == '__main__':
    stuid = raw_input(u'请输入学号：')
    oldPass = raw_input(u'输入旧密码:')
    newPass = raw_input(u'输入新密码:')
    test = DrChPsw(stuid, oldPass, newPass)
    test.chpasswd()
