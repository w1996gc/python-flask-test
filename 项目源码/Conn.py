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
import json

def conn():
    data = {
        "host": "111.173.83.23",
        "user": "root",
        "password": "Wqq@123456",
        "db": "test",
        "charset": "utf8"
    }
    if not os.path.exists("auto.json"):
        json_str = json.dumps(data, indent=4)
        with open("auto.json", "w") as f:
            f.write(json_str)
    else:
        file = open('auto.json', 'rb')
        jsonData = json.load(file)
        host = jsonData['host']
        user = jsonData['user']
        pwd = jsonData['password']
        db = jsonData['db']
        charset = jsonData['charset']
        conn = pymysql.connect(host=host, user=user, password=pwd, db=db, charset=charset)

        cur = conn.cursor()
        return cur,conn
def connect():
    data = {
        "host": "111.173.83.23",
        "user": "root",
        "password": "Wqq@123456",
        "db": "test",
        "charset": "utf8"
    }
    if not os.path.exists("auto.json"):
        json_str = json.dumps(data, indent=4)
        with open("auto.json", "w") as f:
            f.write(json_str)
    else:
        file = open('auto.json', 'rb')
        jsonData = json.load(file)
        host = jsonData['host']
        user = jsonData['user']
        pwd = jsonData['password']
        db = jsonData['db']
        charset = jsonData['charset']
        conn = pymysql.connect(host=host, user=user, password=pwd, db=db, charset=charset)
        cursor = conn.cursor()
        return conn,cursor