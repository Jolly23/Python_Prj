# -*- coding: utf-8 -*-

from flask import render_template
from flask import Blueprint
from flask import request
from flask import url_for
from flask import make_response

from checkevent import checkevent
from chat_api import chatApi

import urllib
import urllib2
from urllib import urlencode
import json
import time
import hashlib
import xml.etree.ElementTree as ET
import re

from app.GetCET.GetCET_flask import *
from app.GetCET.GetName import GetName
from app import db
from app.user.models import regUser
from app.Music.music import *

weixin = Blueprint('weixin', __name__, template_folder = 'templates')

@weixin.route('/weixin',methods=['GET','POST'])
def wechat_auth():
    if request.method == 'GET':
        token='jzp113'
        data = request.args
        signature = data.get('signature','')
        timestamp = data.get('timestamp','')
        nonce = data.get('nonce','')
        echostr = data.get('echostr','')
        s = [timestamp,nonce,token]
        s.sort()
        s = ''.join(s)
        if (hashlib.sha1(s).hexdigest() == signature):
            return make_response(echostr)
    else:
        rec = request.stream.read()
        xml_rec = ET.fromstring(rec)
        tou = xml_rec.find('ToUserName').text
        fromu = xml_rec.find('FromUserName').text
        event = xml_rec.find('Event')
        event_key = xml_rec.find('EventKey')
        content = xml_rec.find('Content')
	    
        
        if content is not None:
	    
            contents = chatApi(content.text, fromu)
	    #contents =  "机器人生病了，但是，敬业的机器人仍然提供，四级，六级，表白墙，成绩单，课表等关键词的相关功能"
	    pattern2 = re.compile(r'[\S\s]*(成绩|成绩单|考的怎么样|考试结果|挂科了|挂了没|我过了么|及格|分数|多少分|考过没)[\S\s]*')
            match2 = pattern2.match(str(content.text))
            if match2:
	    #if content.text == "成绩单":
		url_tmp = url_for('user.gradeList',fromu=fromu,_external=True)
		picUrl_tmp = url_for('static',filename='img/1.png',_external=True)
		print picUrl_tmp
		return render_template('reply_img.xml',
		toUser = fromu,
		fromUser = tou,
		createtime = str(int(time.time())),
		title = "小偲查询---成绩单",
		desc = "快来看看，你挂了科么？"+contents,
		picUrl = picUrl_tmp,
		url = url_tmp
		)
	    pattern2 = re.compile(r'[\S\s]*(课表|上课|下课|课程安排|课程表|我的课)[\S\s]*')
	    match2 = pattern2.match(str(content.text))
	    if match2:
	    #if content.text == "课表":
		url_tmp = url_for('user.courseList',fromu=fromu,_external=True)
		picUrl_tmp = url_for('static',filename='img/2.jpg',_external=True)
		print picUrl_tmp
		return render_template('reply_img.xml',
		toUser = fromu,
		fromUser = tou,
		createtime = str(int(time.time())),
		title = "小偲查询---课表",
		desc = "不逃课的孩子才是好孩子哟~"+contents,
		picUrl = picUrl_tmp,
		url = url_tmp
		)
	    pattern3 = re.compile(r'[\S\s]*(表白|失恋|爱你|你爱我|love|LOVE|喜欢你|想你|你喜欢我|我喜欢你|like|LIKE|表白|表白墙|爱要勇敢的说出来)[\S\s]*')
	    match3 = pattern3.match(str(content.text))
	    if match3:
	    #if content.text == "表白墙":
		url_tmp = url_for('lovewall.loveon',openid=fromu,_external=True)
		picUrl_tmp = url_for('static',filename='img/3.jpg',_external=True)
		return render_template('reply_img.xml',
		toUser = fromu,
		fromUser = tou,
		createtime = str(int(time.time())),
		title = "小偲----表白墙",
		desc = "爱他（她），就告诉他（她）~"+contents,
		picUrl = picUrl_tmp,
		url = url_tmp
		)

	    pattern4 = re.compile(r'[\S\s]*(4级|四级)[\S\s]*')
	    match4 = pattern4.match(str(content.text))
	    pattern5 = re.compile(r'[\S\s]*(6级|六级)[\S\s]*')
	    match5 = pattern5.match(str(content.text))
	    if match4 or match5:
		if match4:
			cet=1	
		else:
			cet=2
		
		contents = u'请绑定后使用'
		if regUser.query.filter_by(openid = fromu).first():
			exist_user = regUser.query.filter_by(openid = fromu).first()
			
			some = GetName(exist_user.username, exist_user.password_urp)
			some.login()
			name = some.get_name()
			contents = get_DLNU_Score(name,cet)
			CETgrade = "查询出错，请核实您输入的信息以及绑定的学号，稍后再试"
			if not (contents["error"]):
				CETgrade = "姓名:	"+contents["name"]+"\n"+"学校:	"+contents["school"]+"\n"+"听力:	"+contents["Listening"]+"\n"+"阅读:	"+contents["Reading"]+"\n"+"写作:	"+contents["Writing"]+"\n"+"总分:	"+contents["Total"]+"\n"+"小偲---------查询"
			contents = CETgrade
	    


	    pattern6 = re.compile(r'[\S\s]*(说话|首|歌曲|语音|歌|MUSIC|music|音乐|声)[\S\s]*')
	    match6 = pattern6.match(str(content.text))
	    if match6:
		openid,title, desc, music_url, thumb_media_id = get_douban_fm(fromu)
		print title, desc, music_url, thumb_media_id
		return render_template('reply_music.xml',
		toUser = fromu,
		fromUser = tou,
		createtime = str(int(time.time())),
		title = title,
		desc = desc,
		MUSIC_Url = music_url,
		HQ_MUSIC_Url = music_url
		)

        elif event.text == 'subscribe':
            key = 'subscribe'
            contents = checkevent(fromu).key_check(key)
        else:
            key = event_key.text
            contents = checkevent(fromu).key_check(key)


        return render_template('reply_text.xml',
        toUser = fromu,
        fromUser = tou,
        createtime = str(int(time.time())),
        content = contents
        )

