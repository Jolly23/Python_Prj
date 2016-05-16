# -*- coding: utf-8 -*-

from sql import *
import sqlite3

import os
os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'


class UrpDb(object):

    @classmethod
    def get_zyh(cls):
        # 专业号
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(s_zyh_sql)
        data = cursor.fetchall()
        conn.close()
        zyh_list = []
        for i in data:
            zyh_list.append(i)
        return zyh_list

    @classmethod
    def get_dh(cls):
        # 取得电话
        conn = connect()
        cursor = conn.cursor()
        cursor.execute(s_dh_sql)
        data = cursor.fetchall()
        conn.close()
        # conn_sqlite = sqlite3.connect('/home/jolly/Documents/Python_Prj/_Study/DB_Study/5/User_dh.db')
        for i in data:
            if isinstance(i[1], str):
                if len(i[1]) == 11:
                    print i
                    # conn_sqlite.execute("INSERT INTO users_dh VALUES ('%s', '%s')" % (i[0], i[1]))
        # conn_sqlite.commit()
        # conn_sqlite.close()

    @classmethod
    def get_info(cls):
        # 取得信息
        zyh_list = cls.get_zyh()

        conn = connect()
        cursor = conn.cursor()
        cursor.execute(s_infoj_sql)
        data = cursor.fetchall()
        conn.close()
        info_list = []
        conn_sqlite = sqlite3.connect('/home/jolly/Documents/Python_Prj/_Study/DB_Study/5/User_dh.db')
        for stu in data:
            for ii in zyh_list:
                if stu[4] == ii[0]:
                    zym = ii[2]
            dh_sql = conn_sqlite.execute('select * from users_dh where UID = "%s"' % stu[2])
            dh_list = dh_sql.fetchall()
            if dh_list:
                info = {
                    'name': stu[0],
                    # 'gender': stu[1],
                    'major': zym,
                    'dh': dh_list[0][1]
                }
                info_list.append(info)
        return info_list


if __name__ == '__main__':
    majors = ('软件工程', '网络工程', '计算机科学与技术', '电子信息工程', '通信工程', '物联网工程',
              '信息与计算科学', '信息与计算科学', '自动化', '测控技术与仪器', '机械设计制造及其自动化',
              '工业工程', '产品设计')

    a = UrpDb()

    b = a.get_info()
    done = []
    for i in b:
        if i['major'] in majors:
            print i['major'], '\t', i['name'], '\t', i['dh']
            done.append(i)

    print len(done)



