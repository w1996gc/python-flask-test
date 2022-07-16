#!/usr/bin/python
# -*- coding: utf-8 _*_
'''
 @File     : query.py
 @Time     : 2022/6/15 17:45
 @Software : PyCharm
 @Author   : Tom
 @Version  : 
'''

import os

import pymysql


def get_mca_conn(sql):
    try:
        conn = pymysql.connect(host='localhost', user='root', password='123456', db='test', port=3306, charset='utf8')
        cur = conn.cursor()
        sql = f"select * from `test`.`hitachi_mca` where TCD= '{sql}'"
        cur.execute(sql)
        data = cur.fetchall()
        errill = data[0][1]
        errreason = data[0][2]
        cur.close()
        conn.close()
        if errreason == '':
            errreason = '暂无'
            return errill, errreason
        return errill, errreason
    except Exception as ee:
        e = '该故障代码不存在，请检查后重新输入'
        return 'Error:{}——{}'.format(e, ee), '程序出错'
    except TimeoutError as err:
        return 'Error:{}'.format(err), '程序超时'
if __name__ == '__main__':
    print(get_mca_conn('10'))