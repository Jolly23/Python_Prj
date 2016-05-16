#coding=utf-8

import requests

def post_data(s,url,data):
    s.get(url)
    params = { 'csrfmiddlewaretoken':s.cookies.get('csrftoken')}
    params.update(data)
    r = s.post(url,data=params)
    return r,s

url_login = 'http://www.heibanke.com/accounts/login/?next=/lesson/crawler_ex02/'
url_form = 'http://www.heibanke.com/lesson/crawler_ex02/'

s= requests.Session()
r,s = post_data(s,url_login,{'username':'test','password':'test123'})
print 'login' , r.status_code

for numPassword in range(30):
    rr,s = post_data(s,url_form,{'username':'Jolly','password':numPassword})
    if rr.text.find(u'密码错误')>0:
        print u'尝试密码 ',numPassword,u' 错误'
        numPassword += 1
    else:
        print rr.text
        print u'密码为:',numPassword
        break