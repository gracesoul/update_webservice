# -*- coding: utf-8 -*-
# @time:2019/5/15 9:35
# Author:殇殇
# @file:test_sendMCode.py
# @fuction: 测试发送验证码接口 断言
import unittest
from ddt import ddt,data
from common.my_log import MyLog
from common.do_excel import DoExcel
from common.do_contants import *
from common.do_suds import DoSuds
import warnings
from common.generate_data import create_ip,create_phone
from common.do_mysql import DoMysql

do_excel = DoExcel(case_dir,'sendMCode')
sendMCode_cases = do_excel.get_data()
log = MyLog(__file__)
@ddt
class TestSendmcode(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        warnings.simplefilter ("ignore", ResourceWarning)
        log.info ('-----开始执行测试用例-----')
        cls.ws_request = DoSuds()
        cls.mysql = DoMysql ()

    @data(*sendMCode_cases)
    def test_sendMCode(self,case):
        log.info('开始执行第{}条测试用例：{}'.format(case.case_id,case.title))

        # 替换excel中的参数化ip的值
        if case.data.find('random_ip')>-1:
            ip = create_ip()
            case.data = case.data.replace('random_ip',ip)

        # 替换Excel中的参数化normal_phone的值
        if case.data.find('random_phone')>-1:
            phone = create_phone ()
            case.data = case.data.replace('random_phone',phone)

        # 替换sql中指定的值
        if case.check_sql and case.check_sql.find('random_phone')>-1:
            case.check_sql = case.check_sql.replace('random_phone',phone)

        resp = self.ws_request.do_suds (case.url, case.data, case.method)
        try:
            self.assertEqual(case.expected,resp)
            do_excel.write_back(case.case_id+1,resp,'Pass') # 将结果写回到数据库中

            # 用例执行通过后，校验数据库，查看影响的行数
            if case.check_sql:
                sql = eval(case.check_sql)['sql1']
                result_by_db = self.mysql.fetch_one(sql)
                print('用例成功后，查询数据库得到的数据是：{}'.format(result_by_db))

        except AssertionError as e:
            do_excel.write_back(case.case_id+1,resp,'Failed')
            log.error('断言出错,信息是：{}'.format(e))
            raise e

    @classmethod
    def tearDownClass(cls):
        log.info('-----测试用例执行完毕-----')
        cls.mysql.close()

if __name__ == '__main__':
    unittest.main()