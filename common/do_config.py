# -*- coding: utf-8 -*-
# @time:2019/5/15 10:04
# Author:殇殇
# @file:do_config.py
# @fuction: 封装操作配置文件的读取
from configparser import ConfigParser
from common.do_contants import *


class ReadConfig:
    def __init__(self,encoding='utf-8'):
        # 打开配置文件
        self.cf = ConfigParser ()
        # 读取配置文件
        self.cf.read(global_dir,encoding=encoding)
        if self.cf.getboolean('switch','on'):
            self.cf.read(test_dir,encoding=encoding)
        else:
            self.cf.read(online_dir,encoding=encoding)

    def get_intvalue(self,section,option):
        return self.cf.getint(section,option)

    def get_strvalue(self,section,option):
        return self.cf.get(section,option)

    def get_boolvalue(self,section,option):
        return self.cf.getboolean(section,option)

    def get_section(self):
        return self.cf.sections()

    def get_option(self,section):
        return self.cf.options(section)




