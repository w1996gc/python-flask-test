#!/usr/bin/python
# -*- coding: utf-8 _*_
'''
 @File     : reposted.py
 @Time     : 2022/5/9 17:53
 @Software : PyCharm
 @Author   : Tom
 @Version  : 
'''

import os

import requests


def baidu_fanyi(word):
    try:
        url = 'https://fanyi.baidu.com/sug'
        data = {'kw': word}  # 你只需要改kw对应的值
        res = requests.post(url, data=data).json()
        pt = res['data'][0]['v']
        return "翻译{}成功,结果为:\n{}".format(word,pt)
    except Exception as e:
        return "翻译{}出错,故障为:\n{}".format(word,e)