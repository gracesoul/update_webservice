# -*- coding: utf-8 -*-
# @time:2019/5/15 15:16
# Author:殇殇
# @file:test_userRegister.py
# @fuction: 测试用户注册接口
from ddt import ddt,data
import unittest
from common.do_suds import DoSuds
from common.do_excel import DoExcel
from common.do_contants import *
from common.generate_data import create_ip,create_phone,create_userid
from common.my_log import MyLog
from common.do_context import Context,replace
from common.do_mysql import DoMysql

log = MyLog(__name__)
do_excel = DoExcel(case_dir,'userRegister')
register_cases = do_excel.get_data ()

@ddt
class TestRegister(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        log.info('------开始执行测试用例-----')
        cls.ws_request = DoSuds ()
        cls.mysql = DoMysql ()

    @data(*register_cases)
    def test_userRegister(self,case):
        log.info('开始执行第{}条测试用例：{}'.format(case.case_id,case.title))
        case.data = replace(case.data)

        # 替换excel中的参数化register_ip的值
        if case.data.find('register_ip')>-1:
            ip = create_ip()
            setattr (Context, 'register_ip', ip)
            case.data = case.data.replace('register_ip',ip)


        # 替换excel中的参数化register_mobile的值
        if case.data.find('register_mobile')>-1:
            phone = create_phone ()
            setattr(Context,'register_mobile',phone)
            case.data = case.data.replace ('register_mobile', phone)

        # 替换excel中的参数化register_name的值
        if case.data.find('register_name')>-1:
            # 随机生成用户id
            userid = create_userid ()
            setattr(Context,'register_name',userid)
            case.data = case.data.replace('register_name',userid)

        # 替换sql中指定的值
        if case.check_sql and case.check_sql.find ('register_mobile') > -1:
            case.check_sql = case.check_sql.replace ('register_mobile', phone)

        # 查询数据库，并且把查询的结果反射到Context类的属性中，方便后面参数调用
        if case.check_sql and case.case_id==4:
            sql = eval(case.check_sql)['sql4']
            time_out_code = self.mysql.fetch_one(sql)['Fverify_code']
            setattr(Context,'time_out_code',time_out_code)
            time_out_mobile = self.mysql.fetch_one(sql)['Fmobile_no']
            setattr(Context,'time_out_mobile',time_out_mobile)

        resp = self.ws_request.do_suds (case.url, case.data, case.method)

        # 判断验证码发送成功后，查询数据库 取到验证码,传到下一个接口的参数中去
        if case.case_id == 1 and resp=='ok':
            sql = eval(case.check_sql)['sql1']
            get_code = self.mysql.fetch_one(sql)['Fverify_code']
            setattr(Context,'code',get_code)
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