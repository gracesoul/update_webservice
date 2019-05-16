# -*- coding: utf-8 -*-
# @time:2019/5/15 9:21
# Author:殇殇
# @file:do_contants.py
# @fuction: 封装操作文件的路径

import os

# print(os.path.abspath(__file__))
# print(os.path.dirname(os.path.abspath(__file__)))
# print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
case_dir = os.path.join(base_dir,'data','case.xlsx')
log_dir = os.path.join(base_dir,'log')
global_dir = os.path.join(base_dir,'config','global.cfg')
online_dir = os.path.join(base_dir,'config','online.cfg')
test_dir = os.path.join(base_dir,'config','test.cfg')
test_case = os.path.join(base_dir,'testcase')
report_file = os.path.join(base_dir,'report')