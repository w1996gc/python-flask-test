#!/usr/bin/python
# -*- coding: utf-8 _*_
'''
 @File     : main_test.py
 @Time     : 2022/12/2 21:07
 @Software : PyCharm
 @Author   : Tom
 @Version  : 
'''
import json
import os
data={
    "print":"hello word"
}
with open('test.json','w')as f:f.write(json.dumps(data,indent=4))