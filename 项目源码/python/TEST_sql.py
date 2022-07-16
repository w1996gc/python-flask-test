#!/usr/bin/python
# -*- coding: utf-8 _*_
'''
 @File     : TEST.py
 @Time     : 2022/6/8 23:06
 @Software : PyCharm
 @Author   : Tom
 @Version  : 
'''

import os
import random
import re

import pymysql
def get_data_clear():
    conn = pymysql.connect(host="127.0.0.1", user="root", password="123456", db="test", charset="utf8")
    cur=conn.cursor()
    sql1=f"truncate table sys_user"
    cur.execute(sql1)
    cur.close()
    conn.close()

def get_date():
    a='16730909857'

    tel=re.match(r"^1[35678]\d{9}$",a)
    print(tel)
def get_conn(n,user,password,mail,photonumber):
    # 建立数据库连接
    conn = pymysql.connect(host="127.0.0.1", user="root", password="123456", db="test", charset="utf8")
    cur=conn.cursor()
    # sql=f"INSERT INTO sys_user VALUES (%s, '%s', '%s', '管理员', '%s', '%s');"%(n,user,password,mail,photonumber)
    sql=f"INSERT INTO `test`.`sys_user` VALUES (2, 'admin', '123456', '管理员', '23456@qq.com', '13552699852')"
    # sql1=f"select * from sys_user"
    # print(sql)
    cur.execute(sql)
    conn.commit()
    # cur.execute(sql1)
    # data = cur.fetchall()
    # print(data)
    cur.close()
    conn.close()
def main():
    try:
        n=random.randint(1,10)
        get_conn(n,'admin','123456','23456@qq.com','13552699852')
    except Exception as e:
        print(e)
        a=random.randint(1,10)
        b=1
        n=a+b+1
        get_conn(n, 'admin', '123456', '23456@qq.com', '13552699852')

if __name__ == '__main__':
    main()