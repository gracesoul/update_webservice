# -*- coding: utf-8 -*-
# @time:2019/5/15 17:12
# Author:殇殇
# @file:test_verifiedUserAuth.py
# @fuction: 测试实名认证的接口

import unittest
from ddt import ddt,data
from common.do_excel import DoExcel
from common.do_contants import *
from common.my_log import MyLog
from common.do_context import Context,replace
from common.do_suds import DoSuds
from common.generate_data import create_ip,create_userid,create_phone,create_name,create_idcard
from common.do_mysql import DoMysql
import warnings

log = MyLog (__name__)
do_excel = DoExcel(case_dir,'verifiedUserAuth')
userAuth_cases = do_excel.get_data ()



@ddt
class TestVerifiedUserAuth(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        warnings.simplefilter ("ignore", ResourceWarning)
        log.info ('-----开始执行测试用例-----')
        cls.ws_request = DoSuds ()
        cls.mysql = DoMysql ()

    @data(*userAuth_cases)
    def test_userAuth(self,case):
        log.info('开始执行第{}条测试用例：{}'.format(case.case_id,case.title))
        case.data = replace(case.data)

        # 替换excel中的参数化register_ip的值（ip地址）
        if case.data.find('register_ip')>-1:
            ip = create_ip ()
            setattr(Context,'register_ip',ip)
            case.data = case.data.replace('register_ip',ip)

        # 替换excel中的参数化register_mobile的值（手机号）
        if case.data.find('register_mobile')>-1:
            phone = create_phone ()
            setattr(Context,'register_mobile',phone)
            case.data=case.data.replace('register_mobile',phone)

        # 替换excel中的参数化register_name的值(唯一的用户id)
        if case.data.find('register_name')>-1:
            userid = create_userid ()
            setattr(Context,'register_name',userid)
            case.data = case.data.replace('register_name',userid)

        # 替换sql中指定的register_mobile值(手机号)
        if case.check_sql and case.check_sql.find('register_mobile')>-1:
            case.check_sql = case.check_sql.replace('register_mobile',phone)

        # 替换sql中指定的register_name值（用户id）
        if case.check_sql and case.check_sql.find('register_name')>-1:
            case.check_sql = case.check_sql.replace('register_name',userid)

        # 替换excel中的参数化username的值（真实姓名）
        if case.data.find('username')>-1:
            name = create_name ()
            case.data = case.data.replace('username',name)

        # 替换excel中的参数化card_id的值(身份证)
        if case.data.find('card_id')>-1:
            idcard = create_idcard ()
            setattr(Context,'card_id',idcard)
            case.data = case.data.replace('card_id',idcard)

        # 替换sql中指定的true_name值(真实姓名)
        if case.check_sql and case.check_sql.find('username')>-1:
            case.check_sql = case.check_sql.replace('username',name)

        resp = self.ws_request.do_suds(case.url,case.data,case.method)
        log.info('响应的结果是：{}'.format(resp))

        # 通过操作数据库(通过手机号找验证码)，获取验证码
        if case.case_id == 1 and resp =='ok':
            sql = eval(case.check_sql)['sql1']
            get_code = self.mysql.fetch_one(sql)['Fverify_code']
            setattr(Context,'code',get_code)

        # 通过操作数据库（通过注册的用户名user_id去找），获取用户的Uid
        if case.case_id == 2 and resp =='ok':
            sql = eval(case.check_sql)['sql2']
            get_uid = self.mysql.fetch_one(sql)['Fuid']
            setattr(Context,'user_id',str(get_uid))
            print('得到的id是：{}'.format(get_uid))

        # 校验数据库 查看数据库的影响行数
        if case.case_id==3 and resp=='ok':
            sql = eval(case.check_sql)['sql3']
            print('执行的sql语句是：{}'.format(sql))
            get_result = self.mysql.fetch_one(sql)
            print('通过数据库，返回的数据是：{}'.format(get_result))

        try:
            self.assertEqual(case.expected,resp)
            do_excel.write_back(case.case_id+1,resp,'Pass')
        except AssertionError as e:
            do_excel.write_back(case.case_id+1,resp,'Failed')
            log.error('断言出错：{}'.format(e))
            raise e

    @classmethod
    def tearDownClass(cls):
        log.info('-----测试用例执行完毕-----')
        cls.mysql.close()


if __name__ == '__main__':
    unittest.main()
