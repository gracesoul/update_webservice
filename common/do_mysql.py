# -*- coding: utf-8 -*-
# @time:2019/5/15 13:57
# Author:殇殇
# @file:do_mysql.py
# @fuction: 封装操作数据库的数据的读取与操作
import pymysql
from common.do_config import ReadConfig

config = ReadConfig ()


class DoMysql:
    def __init__(self):
        db_host = config.get_strvalue('db','db_host')
        db_port = config.get_intvalue('db','db_port')
        db_username = config.get_strvalue('db','db_username')
        db_password = config.get_strvalue('db','db_password')
        # 打开建立数据库的连接
        self.db = pymysql.Connect(host=db_host,port=db_port,user=db_username,password=db_password,charset='utf8')
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor) # 创建字典形式的一个游标对象

    def fetch_one(self,sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
        return self.cursor.fetchone()

    def fetch_all(self,sql):
        try:
            self.cursor.execute(sql)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.db.close()


if __name__ == '__main__':
    sql = 'select max(Fmobile_no) from sms_db_20.t_mvcode_info_0 ;'
    sql1 = 'select * from sms_db_54.t_mvcode_info_0 where Fmobile_no = 18814296054;'
    mysql = DoMysql()
    result = mysql.fetch_one(sql1)
    print('得到的结果是：{}，类型是：{}'.format(result,type(result)))
