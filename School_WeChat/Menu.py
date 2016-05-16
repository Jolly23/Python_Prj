#!/usr/bin/python
#coding=utf-8
import requests
import json

GetAT_URL = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wx16259cea4606e0ce&secret=32925f31b9e4950f1f982cd7ad084bae'


POSTDATA = '''{
     "button":[
     	{
          "type":"click",
          "name":"近期成绩",
          "key":"SSCORE"
      	},
    	
      	{
           "name":"Test",
           "sub_button":[
            {
               	"type":"click",
          		"name":"全部成绩",
          		"key":"ALLSCORE"
            },
            {
               "type":"click",
               "name":"课程号",
               "key":"Courses"
            },
            {
               "type":"view",
               "name":"Score",
               "url":"http://210.30.7.100:8088/"
            }]
       	},

      	{
          "type":"click",
          "name":"Drcom",
          "key":"Drcom"
      	}
    ]
 }'''

s = requests.Session()

Ret = s.get(url=GetAT_URL)
GetJson = json.loads(Ret.text)
Access_Token = GetJson['access_token']

CreateMenu_URL = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token=' + Access_Token
CancelMenu_URL = 'https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=' + Access_Token


#Req = s.get(url=CancelMenu_URL)                    #关闭菜单
Req = s.post(url=CreateMenu_URL,data=POSTDATA)      #创建菜单

print Req.text
