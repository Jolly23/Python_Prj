# -*- coding: utf-8 -*-
from datetime import datetime

import cx_Oracle

ORL_DATABASE_URI = ['210.30.1.11', '1521', 'dlnu10g', 'jw1', '345678']

# 学生个人电话
s_dh_sql = '''SELECT XH, DH
FROM NEWJW.XS_GRXXB WHERE XH LIKE '2013%'
'''

# 学生个人信息
s_info_sql = '''SELECT XM, YWXM, SFZH, XB, XH, MZDM, JG, BYZX, GKZF, XSH, ZYH, BJH, XQH
FROM NEWJW.XS_XJB WHERE XH LIKE '2013%'
'''

# 学生个人信息
s_infoj_sql = '''SELECT XM, XB, XH, XSH, ZYH
FROM NEWJW.XS_XJB WHERE XH LIKE '2013%'
'''

# 专业号码
s_zyh_sql = '''SELECT ZYH, XSH, ZYM
FROM NEWJW.CODE_ZYB
'''


def connect():
    dsn_tns = cx_Oracle.makedsn(*ORL_DATABASE_URI[:3])
    conn = cx_Oracle.connect(ORL_DATABASE_URI[-2], ORL_DATABASE_URI[-1], dsn_tns)
    return conn


def term_year():
    """

    :return: '2015-2016-2-1' 16.5.6 第二学期
    """
    now = datetime.now()
    now_year, now_month = now.year, now.month
    term = 1
    if now_month in range(3, 9):
        now_year -= 1
        term = 2
    if now_month in range(3):
        now_year -= 1
    return '{0}-{1}-{2}-1'.format(now_year, now_year+1, term)
