# -*- coding: utf-8 -*-
# @time:2019/5/14 14:53
# Author:殇殇
# @file:my_log.py
# @fuction: 封装操作日志文件

import logging
from common.do_contants import *

class MyLog:
    def __init__(self,name):
        self.name = name

    def my_log(self,level,msg):
        # 1.创建日志收集器
        my_logger = logging.getLogger(self.name)
        # 2.设置收集器的等级
        my_logger.setLevel('DEBUG')
        # 3.设置输出格式
        formater = logging.Formatter('%(asctime)s-' '%(name)s-' '[%(levelname)s]-' '[%(filename)s:%(lineno)d]-' '[日志信息]:%(message)s')
        # 4.添加输出渠道--》控制台
        sh = logging.StreamHandler ()
        sh.setLevel('DEBUG')
        sh.setFormatter(formater)
        # 4.2 添加输出渠道--》指定文件
        fh = logging.FileHandler(log_dir + '/text.log',encoding='utf-8')
        fh.setLevel('DEBUG')
        fh.setFormatter(formater)
        # 5.日志收集器与输出渠道进行交接
        my_logger.addHandler(sh)
        my_logger.addHandler(fh)
        if level == 'DEBUG':
            my_logger.debug(msg)
        elif level == 'INFO':
            my_logger.info(msg)
        elif level== 'WARNING':
            my_logger.warning(msg)
        elif level =='ERROR':
            my_logger.error(msg)
        else:
            my_logger.critical(msg)

        # 6.移除
        my_logger.removeHandler(sh)
        my_logger.removeHandler(fh)

    def debug(self,msg):
        self.my_log('DEBUG',msg)

    def info(self,msg):
        self.my_log('INFO',msg)

    def warning(self,msg):
        self.my_log('WARNING',msg)

    def error(self,msg):
        self.my_log('ERROR',msg)

    def critical(self,msg):
        self.my_log('CRITICAL',msg)


if __name__ == '__main__':
    log = MyLog(__file__)
    log.debug('这是测试数据！')

