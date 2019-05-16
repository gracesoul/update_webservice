# -*- coding: utf-8 -*-
# @time:2019/5/14 13:30
# Author:殇殇
# @file:do_suds.py
# @fuction: 封装请求webservice的请求方法

from suds.client import Client
from suds import WebFault
from common.do_config import ReadConfig
config = ReadConfig() # 实例化对象


class DoSuds:
    def do_suds(self,url,data,method):
        url = config.get_strvalue('api','pre_url')+url # 拼接路径
        if type(data)==str:  # Excel中的取出的数据是 str 将其转化为 dict (使用eval()函数)
            data = eval(data)
        print('请求的路径是：{}'.format(url))
        print('请求的数据是：{}'.format(data))
        # 建立一个客户端
        client = Client(url)
        try:
            resp = eval("client.service.{0}({1})".format(method,data))
            print ('响应的返回码；{}'.format (resp.retCode))
            print ('响应的返回信息：{}'.format (resp.retInfo))
            result_msg = resp.retInfo
            # print('响应的类型是：{}'.format(type(result_msg)))
        except WebFault as e:
            print ('返回的异常信息是：{}'.format (e.fault.faultstring))
            result_msg = e.fault.faultstring
            # print ('响应的类型是：{}'.format (type (result_msg)))
            # result_msg的数据类型是：<class 'suds.sax.text.Text'>
            # 将其写回到Excel 必须是str 所以使用强转化
        return str(result_msg)



if __name__ == '__main__':
    url = '/sms-service-war-1.0/ws/smsFacade.ws?wsdl'
    data = {"client_ip":"127.0.0.1","tmpl_id":"1","mobile":"1553621420"}
    result = DoSuds().do_suds(url,data,"sendMCode")
    print(result)








