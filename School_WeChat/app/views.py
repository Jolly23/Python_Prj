#!/usr/bin/python
#coding=utf-8

import time
import hashlib
import string
from app import db
from flask import Flask,request,make_response,render_template,flash,url_for
from app import app
from xml.etree import ElementTree
from forms import LoginForm, EvaluationForm
from models import regUser
from Net_Drcom.GetUserDrcom import Drcom
from URP_Edu.GetUserScore import URP_GetScore
from URP_Edu2.GetUserCourses import GetUserCourses


# WeChat Request
@app.route('/',methods=['GET','POST'])
def index():
    #WeChat_API_Check, method of request is GET
    if request.method == 'GET':
        return WeChatAPI_Check(request)

    #User Call, merhod of request is POST, data is XML
    else:
        Xml_Recv = ElementTree.fromstring(request.data)
        MyID = Xml_Recv.find("ToUserName").text
        FromUserID = Xml_Recv.find("FromUserName").text
        MsgType = Xml_Recv.find("MsgType").text
        if MsgType == 'text':
            TextMsg = Xml_Recv.find("Content").text
            return Dispose_Text_Msg(FromUserID,MyID,TextMsg)
        if MsgType == 'event':
            EventKey = Xml_Recv.find("EventKey").text
            return Dispose_Event_Req(FromUserID,MyID,EventKey)


# User_Bind
@app.route('/login/<string:openid>', methods = ['GET', 'POST'])
def login(openid=None):
    openid = openid
    form = LoginForm()
    if form.validate_on_submit() and openid:
        EX_USER = regUser.query.filter_by(openid = openid).first()
        if EX_USER:
            db.session.delete(EX_USER)
            db.session.commit()
        USER = regUser(openid, form.username.data, form.password_urp.data,form.password_drcom.data)
        db.session.add(USER)
        db.session.commit()
        return render_template('succeed.html')
    return render_template('login1.html',
        title = 'Sign In',
        form = form)


def Dispose_Text_Msg(FromUserID,MyID,TextMsg):
    rText = ''
    if u'成绩' in TextMsg:
        USER = regUser.query.filter_by(openid = FromUserID).first()
        if USER:
            ScoreInfo = URP_GetScore(USER.username,USER.password_urp)
            ScoreInfoList = ScoreInfo.GetRecentScore()
            for Info in ScoreInfoList:
                if u'未评估' in Info['COURSE_SCORE']:
                    continue
                rText = rText + Info['COUSER_NAME'] + '---' +  Info['COURSE_SCORE'] + '\n'
        else:
            return AskForBind(FromUserID,MyID)

    elif u'解' in TextMsg:
        USER = regUser.query.filter_by(openid = FromUserID).first()
        if USER:
            db.session.delete(USER)
            db.session.commit()
            rText = u'解绑成功！'
        else:
            rText = u'还没绑定呢'

    elif u'网' in TextMsg or u'流量' in TextMsg:
        USER = regUser.query.filter_by(openid = FromUserID).first()
        if USER:
            aa = Drcom(USER.username,USER.password_drcom)
            rText = aa.RetDrcomInfo()
        else:
            return AskForBind(FromUserID, MyID)

    elif u'离线' in TextMsg:
        USER = regUser.query.filter_by(openid = FromUserID).first()
        if USER:
            aa = Drcom(USER.username,USER.password_drcom)
            rText = aa.logout()
        else:
            return AskForBind(FromUserID, MyID)

    elif u' ' in TextMsg:
        Info = TextMsg.split()
        if len(Info) == 3:
            EX_USER = regUser.query.filter_by(openid = FromUserID).first()
            if EX_USER:
                db.session.delete(EX_USER)
                db.session.commit()
            USER = regUser(FromUserID, Info[0], Info[1],Info[2])
            check_urp = URP_GetScore(Info[0],Info[1])
            if check_urp.AccountCheck():
                check_drcom = Drcom(Info[0],Info[2])
                if check_drcom.AccountCheck():
                    db.session.add(USER)
                    db.session.commit()
                    return RetText(FromUserID,MyID,u'绑定成功!')
                else:
                    return RetText(FromUserID,MyID,u'校园网密码错误，绑定失败!')
            else:
                return RetText(FromUserID,MyID,u'综合教务密码错误，绑定失败!')
        else:
            return RetText(FromUserID,MyID,u'如需绑定，请按照格式要求输入：学号 综合教务密码 校园网密码!')

    else:
        rText = u'赵磊还没教我怎么说话，So...我也不知道你说“%s”是啥意思～' % (TextMsg)

    return RetText(FromUserID,MyID,rText)


def Dispose_Event_Req(FromUserID,MyID,EventKey):
    rText = ''
    if EventKey == 'SSCORE':
        USER = regUser.query.filter_by(openid = FromUserID).first()
        if USER:
            ScoreInfo = URP_GetScore(USER.username,USER.password_urp)
            ScoreInfoList = ScoreInfo.GetRecentScore()
            for Info in ScoreInfoList:
                if u'未评估' in Info['COURSE_SCORE']:
                    continue
                rText = rText + Info['COUSER_NAME'] + '---' +  Info['COURSE_SCORE'] + '\n'
        else:
            return AskForBind(FromUserID,MyID)

    elif EventKey == 'ALLSCORE':
        USER = regUser.query.filter_by(openid = FromUserID).first()
        if USER:
            ScoreInfo = URP_GetScore(USER.username,USER.password_urp)
            ScoreInfoList = ScoreInfo.GetAllScore()
            for Info in ScoreInfoList:
                if u'未评估' in Info['COURSE_SCORE']:
                    continue
                rText = rText + Info['COUSER_NAME'] + '---' +  Info['COURSE_SCORE'] + '\n'
        else:
            return AskForBind(FromUserID,MyID)

    elif EventKey == 'Drcom':
        USER = regUser.query.filter_by(openid = FromUserID).first()
        if USER:
            aa = Drcom(USER.username,USER.password_drcom)
            rText = aa.RetDrcomInfo()
        else:
            return AskForBind(FromUserID,MyID)

    elif EventKey == 'Courses':
        USER = regUser.query.filter_by(openid = FromUserID).first()
        if USER:
            aa = GetUserCourses(USER.username,USER.password_urp)
            rText = aa.GetCourse()
        else:
            return AskForBind(FromUserID,MyID)

    return RetText(FromUserID,MyID,rText)


def AskForBind(UserID,MyID):
    Bind_URL = url_for('login',openid=UserID,_external=True)
    rText = u'<a href="%s">点我绑定</a>' % Bind_URL
    #rText = u'''
    #        页面绑定目前还存在Bug没有解决，小长假，程序员也不在了，为了保证程序还能稳定的运行在阿里云服务器，给同学提供服务，所以我们换一种绑定方式：\n
    #        如需绑定，请用文字发送：学号 综合教务密码 校园网密码（空格隔开）\n
    #        感谢你们的耐心，赵磊回来一定迅速解决这个问题～
    #        '''
    return RetText(UserID,MyID,rText)



def RetText(ToUserID,FromMyID,rText):
    reply = "<xml>" \
            "<ToUserName><![CDATA[%s]]></ToUserName>" \
            "<FromUserName><![CDATA[%s]]></FromUserName>" \
            "<CreateTime>%s</CreateTime>" \
            "<MsgType><![CDATA[text]]></MsgType>" \
            "<Content><![CDATA[%s]]></Content>" \
            "<FuncFlag>0</FuncFlag>" \
            "</xml>"
    response = make_response( reply % (ToUserID, FromMyID, str(int(time.time())), rText ) )
    response.content_type = 'application/xml'
    return response


def WeChatAPI_Check(request):
    token = 'Jolly23'
    query = request.args

    signature = query.get('signature','')
    timestamp = query.get('timestamp','')
    nonce = query.get('nonce','')
    echostr = query.get('echostr','')

    CheckStr = [timestamp,nonce,token]
    CheckStr.sort()
    CheckStr = ''.join(CheckStr)

    if(hashlib.sha1(CheckStr).hexdigest() == signature):
        return make_response(echostr)
