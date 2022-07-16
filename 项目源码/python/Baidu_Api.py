#!/usr/bin/python
# -*- coding: utf-8 _*_
'''
 @File     : Baidu_Api.py
 @Time     : 2022/5/9 20:27
 @Software : PyCharm
 @Author   : Tom
 @Version  : 
'''

import os
import time
import tkinter as tk

import requests

# url='https://fanyi-cdn.cdn.bcebos.com/static/translation/img/favicon/favicon_d87cd2a.ico'
# res=requests.get(url)
# print(res.content)
text='你好'
shijian=int(time.time())
url="https://fanyi.sogou.com/reventondc/synthesis?text={}&speed=1&lang=zh-CHS&from=translateweb&speaker=6".format(text)
text=requests.get(url)
textproject='textproject'
if not os.path.exists(textproject):
    os.mkdir(textproject)
path='./textproject/'+str(shijian)+'.mp3'
with open(path, 'wb') as f:
    f.write(text.content)

