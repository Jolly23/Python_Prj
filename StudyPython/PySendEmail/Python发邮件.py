#!/usr/bin/python
#coding=utf-8
from email.mime.text import MIMEText
from email import encoders
from email.header import Header
from email.utils import parseaddr, formataddr
import smtplib


def __format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(
        (
            Header(name, 'utf-8').encode(), addr.encode('utf-8') if isinstance(addr, unicode) else addr
        )
    )

from_addr = 'pilot_lei@foxmail.com'
passwd = 'Aston77Martin'
SMTP_Server = 'smtp.qq.com'
Sendto = '903221074@qq.com'

msg = MIMEText('Hallo,Send by Python...', 'plain', 'utf-8')
msg['From'] = __format_addr(u'Jolly_Python<%s>' % from_addr)
msg['To'] = __format_addr(u'管理员<%s>' % Sendto)
msg['Subject'] = Header(u'来自赵磊的Python', 'utf-8').encode()

server = smtplib.SMTP(SMTP_Server, 25)
server.set_debuglevel(1)
server.login(from_addr, passwd)
server.sendmail(from_addr, [Sendto], msg.as_string())

server.quit()
