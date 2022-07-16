#!/usr/bin/python
# -*- coding: utf-8 _*_
'''
 @File     : query.py
 @Time     : 2022/6/14 21:14
 @Software : PyCharm
 @Author   : Tom
 @Version  : 
'''

import os
from flask import Flask, render_template
import pymysql

app = Flask(__name__)

conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='1234',
    db='jxgl',
    charset='utf8'
)


@app.route('/')
def hello_world():
    cur = conn.cursor()

    sql = "select * from student"
    cur.execute(sql)
    content = cur.fetchall()

	# 获取表头
    sql = "SHOW FIELDS FROM student"
    cur.execute(sql)
    labels = cur.fetchall()
    labels = [l[0] for l in labels]

    return render_template('index.html', labels=labels, content=content)


if __name__ == '__main__':
    app.run()

