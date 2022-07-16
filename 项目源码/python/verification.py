#!/usr/bin/python
# -*- coding: utf-8 _*_
'''
 @File     : verification.py
 @Time     : 2022/6/9 14:10
 @Software : PyCharm
 @Author   : Tom
 @Version  : 
'''

import os
import urllib.parse
import urllib.request


url='http://106.ihuyi.com/webservice/sms.php?method=Submit'
values={
    'account':'C50078533',
    'password':'5d09cb93f6b1e9989db4977c2b6ef303',
    'mobile' : '18506165137',
    "content" :"你的验证码是:265345。请不要把验证码泄露给别人。",
    'format':'json'
}
params=urllib.parse.urlencode(values).encode('utf-8')
head=urllib.request.Request(url,data=params)
response=urllib.request.urlopen(head)
res=response.read()
print(res.decode('utf-8'))