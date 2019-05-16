# -*- coding: utf-8 -*-
# @time:2019/5/15 11:21
# Author:殇殇
# @file:generate_data.py
# @fuction: 封装不同的需要生成的数据 简化case层的代码

from faker import Faker
# Faker，能够为你产生各种伪装数据的第三方库
import random,string

faker = Faker (locale='zh-CN')


def create_ip():
    # 随机生成IP地址，并且反射到Context类的属性中，方便后面参数调用
    ip = faker.ipv4()
    return ip


def create_phone():
    # 随机生成手机号码 因为分库分表 所以固定第后三位
    phone = random.choice (['139', '188', '177', '136', '158', '150'])\
    +''.join(random.sample(string.digits,5))+'054'
    return phone


def create_name():
    # 随机生成用户名，并且反射到Context类的属性中，方便后面参数调用
    name = faker.name ()
    return name


def create_idcard():
    # 随机生成身份证号
    id_card = faker.ssn ()
    return id_card


def create_userid():
    # 随机生成用户名（用户id）
    user_id = faker.user_name()
    return user_id

# 随机生成银行卡号
def create_bankcard():
    id_code_list = [2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1]
    AAA = random.randint (0, 999)
    BBB = random.randint (0, 999)
    CCC = random.randint (0, 999999)
    result = '621700' + str (AAA).zfill (3) + str (BBB).zfill (3) + str (CCC).zfill (6)
    random_cardid = result + str (sum ([a * b for a, b in zip (id_code_list, [int (a) for a in result])]) % 10)
    return random_cardid

if __name__ == '__main__':
    # ip = create_ip ()
    # print('ip的值：{}，类型：{}'.format(ip,type(ip)))
    # phone = create_phone()
    # print(phone)
    # print(create_name())
    # print(create_idcard())
    # print(create_userid())
    # print (faker.credit_card_number ())  # 随机信用卡号
    print(create_bankcard())