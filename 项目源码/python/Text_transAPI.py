#!/usr/bin/python
# -*- coding: utf-8 _*_
'''
 @File     : Text_transAPI.py
 @Time     : 2022/5/9 20:15
 @Software : PyCharm
 @Author   : Tom
 @Version  : 
'''

# This code shows an example of text translation from English to Simplified-Chinese.
# This code runs on Python 2.7.x and Python 3.x.
# You may install `requests` to run this code: pip install requests
# Please refer to `https://api.fanyi.baidu.com/doc/21` for complete api document
import sys

import requests
import random
import json
from hashlib import md5
def main():
    while True:
        print("1,英语译中文\t2,中文译英文\t其他退出")
        num = input("请输入您要译的语言：")
        if num == '1':
            # from_lang = 'en'
            # to_lang =  'zh'
            # query=input('请输入要翻译的内容：')
            from_lang = 'en'
            to_lang =  'zh'
            query=input('请输入要翻译的内容：')
            run=BaiduFanyi(query,from_lang,to_lang)
        elif num == '2':
            from_lang = 'zh'
            to_lang = 'en'
            query=input('请输入要翻译的内容：')
            run=BaiduFanyi(query,from_lang,to_lang)
        else:
            sys.exit()
class BaiduFanyi():
    def __init__(self,query,from_lang,to_lang):
        # Set your own appid/appkey.
        appid = '20220509001209410'
        appkey = 'rhQuJj1eugskVi3eGKsw'

        # For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
        from_lang=from_lang
        to_lang=to_lang
        endpoint = 'http://api.fanyi.baidu.com'
        path = '/api/trans/vip/translate'
        url = endpoint + path

        # query = 'Hello World! This is 1st paragraph.\nThis is 2nd paragraph.'
        # query='I am English teacher'

        # Generate salt and sign
        salt = random.randint(32768, 65536)
        sign = self.make_md5(appid + query + str(salt) + appkey)
        # Build request
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

        # Send request
        r = requests.post(url, params=payload, headers=headers)
        result = r.json()

        # Show response
        pt = json.dumps(result, indent=4, ensure_ascii=False)
        pt = json.loads(pt)
        self.date_to_str(pt)

    def date_to_str(self,pt):
        # print(pt)
        pnt = pt['trans_result']
        # print(pnt)
        for v in pnt:
            pst=v['dst']
            print(pst)
            return pst
    def make_md5(self,s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()

if __name__ == '__main__':
    main()




