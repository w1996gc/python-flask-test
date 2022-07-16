#!/usr/bin/python
# -*- coding: utf-8 _*_
'''
 @File     : wtest.py
 @Time     : 2022/7/13 23:22
 @Software : PyCharm
 @Author   : Tom
 @Version  : 
'''

import os

import pymysql


def create_s1():
    conn = pymysql.connect(host="127.0.0.1", user="root", password="123456", db="mysql", charset="utf8")
    cur = conn.cursor()
    sql = f"show databases"
    cur.execute(sql)
    res = cur.fetchall()

    labels = [l[0] for l in res]
    cur.close()
    conn.close()
    return labels
print(create_s1())
