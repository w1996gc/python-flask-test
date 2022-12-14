#!/usr/bin/python
# -*- coding: utf-8 _*_
'''
 @File     : MyEncoder.py
 @Time     : 2022/12/14 21:11
 @Software : PyCharm
 @Author   : Tom
 @Version  : 
'''
import datetime
import os
import json
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            print("MyEncoder-datetime.datetime")
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        if isinstance(obj, int):
            return int(obj)
        elif isinstance(obj, float):
            return float(obj)
        #elif isinstance(obj, array):
        #    return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)