#!/usr/bin/env python
# -*- conding: UTF-8 -*-
import urllib3
import requests
from bs4 import BeautifulSoup

def content(url):
    r=url
    response=requests.get(r)
    html=response.text
    bf=BeautifulSoup(html,"lxml")
    texts=bf.find("div",id="box_con")
    return texts.text 

if __name__=='__main__':
    r='https://www.xbiquge.so/book/46515/28465956.html'

    response=requests.get(r)
    html=response.text
    bf=BeautifulSoup(html,"lxml")
    texts=bf.find("div",id="box_con")
    # print(texts)
    texts=texts.find_all("a")
    # print(texts)
    sum=0
    names=[]
    urls=[]
    for i in texts:
        names.append(i.string)
        urls.append(i.get('href'))
    for i in range(len(names)):
        url='https://www.xbiquge.so'+urls[i]
        word=content(url)
        with open('乘龙快婿/'+str(names[i])+'.txt',"a")as f:
            f.write(word)


    print("suessess")
'''    
echo "# python-flask-test" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/w1996gc/python-flask-test.git
git push -u origin main
error: src refspec master does not match any
OpenSSL SSL_read: Connection was reset, errno 10054
'''
