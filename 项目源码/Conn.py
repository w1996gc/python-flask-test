#!/usr/bin/python
# -*- coding: utf-8 _*_
'''
 @File     : Conn.py
 @Time     : 2022/7/13 9:02
 @Software : PyCharm
 @Author   : Tom
 @Version  : 
'''

import os
import pymysql

def conn():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='test', charset='utf8')
    cur = conn.cursor()
    return cur,conn
def connect():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='123456', db='test', charset='utf8')
    cursor = conn.cursor()
    return conn,cursor