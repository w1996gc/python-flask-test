#!/usr/bin/env python
# -*- conding: UTF-8 -*-


import requests
from bs4 import BeautifulSoup

def content(url):
    r=url
    response=requests.get(r)
    html=response.text
    bf=BeautifulSoup(html,"lxml")
    texts=bf.find("div",id="content")
    return texts.text 

if __name__=='__main__':
    r='https://www.xbiquge.so/book/46515/'

    response=requests.get(r)
    html=response.text
    bf=BeautifuiSoup(html,"lxml")