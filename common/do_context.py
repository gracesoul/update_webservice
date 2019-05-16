# -*- coding: utf-8 -*-
# @time:2019/5/15 13:23
# Author:殇殇
# @file:do_context.py
# @fuction: 操作参数化的替换与初始化要复用的属性（下一个接口依赖与上一个接口的结果）
from common.do_config import ReadConfig
import re,configparser

config = ReadConfig ()

class Context:
    register_ip=None
    register_mobile=None
    register_name=None
    code = None
    time_out_code=None
    time_out_mobile = None
    card_id = None
    user_id = None
    bank_idcard = None
    username =None



def replace(data):
    p = '#(.*?)#'
    while re.search(p,data): # 扫描字符串，寻找与模式匹配的字符串,返回匹配对象，如果没有找到匹配，则为None
        find_origin = re.search(p,data)
        find_key = find_origin.group(1)
        try:
            # 如果key在配置文件中 通过key 取value的值
            find_value = config.get_strvalue ('data', find_key)
        except configparser.NoOptionError as e :
            # key不在配置文件中，在Context类中
            if hasattr(Context,find_key):
                find_value = getattr(Context,find_key)
            else:
                print('找不到参数化的值')
                raise e
        data = re.sub(p,find_value,data,count=1)
    return data

