#!/usr/bin/python
# -*- coding: utf-8 _*_
'''
 @File     : Listen_novel_in_web.py
 @Time     : 2022/5/14 23:41
 @Software : PyCharm
 @Author   : Tom
 @Version  : 1.1
'''
import threading
import time

import pyttsx3
import requests
import parsel
import os

from bs4 import BeautifulSoup
from flask import Flask, Blueprint, render_template, request



dft_blueprint = Blueprint('default', __name__)
listen_dir='ListenNovel'
def novel_book():
    engine = pyttsx3.Engine()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 305)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', 1.5)
    voices = engine.getProperty('voices')
    for voice in voices:
        site='id = {} \nname = {} \n'.format(voice.id, voice.name)
    engine.setProperty('Sin-ji', "com.apple.speech.synthesis.voice.alice")
    voice = engine.getProperty('voice')
    url = "https://www.777zw.net/1/1429/"
    response = requests.get(url)
    responses = response.text.encode('iso-8859-1').decode('gbk')
    selector = parsel.Selector(responses)
    novel_name = selector.css('#info h1::text').get()  # 小说名
    href = selector.css('#list dd a::attr(href)').getall()  # 小说章节
    state='done'
    for link in href:
        link_url = url + link
        response_1 = requests.get(link_url)
        responses_1 = response_1.text.encode('iso-8859-1').decode('gbk')
        selecter_1 = parsel.Selector(responses_1)
        title_name = selecter_1.css('.bookname h1::text').get()  # 小说章节
        content_list = selecter_1.css('#content::text').getall()  # 小说内容
        content = '\n'.join(content_list)
        listen_text=content
        state='normal'
        # print(listen_text)
        # engine.say(listen_text)
        # engine.runAndWait()
        # engine.stop()
        time.sleep(5)
        return novel_name,title_name,listen_text,state


def listen_data(link_url):
    print('222',link_url)
    engine = pyttsx3.Engine()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 305)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', 1.5)
    voices = engine.getProperty('voices')
    for voice in voices:
        site='id = {} \nname = {} \n'.format(voice.id, voice.name)
    engine.setProperty('Sin-ji', "com.apple.speech.synthesis.voice.alice")
    voice = engine.getProperty('voice')
    global title_name, listen_text#,link_url
    url = "https://www.777zw.net/1/1429/"
    response = requests.get(url)
    responses = response.text.encode('iso-8859-1').decode('gbk')
    selector = parsel.Selector(responses)
    novel_name = selector.css('#info h1::text').get()  # 小说名'小说名'#


    text = requests.get(link_url).text
    soup = BeautifulSoup(text, 'html.parser')
    title_name=soup.select('#nr_title')[0].text
    listen_text=soup.select('#nr1')[0].text

    # engine.say(listen_text)
    # engine.runAndWait()
    # engine.stop()
    state='normal'
    return novel_name,title_name,listen_text,state


@dft_blueprint.route('/playlisten',methods=['GET','POST'])
def listenplay():
    if request.method == 'GET':
        t=threading.Thread(target=novel_book)
        t.start()
        novel_name, title_name, listen_text,state = novel_book()
        return render_template('ListenBook.html',content_text=listen_text)
@dft_blueprint.route('/sourch',methods=['GET','POST'])
def sourch_book():
    if request.method == 'GET'or request.method == 'POST':

        return render_template('sourch.html',content='hello word',state='normal',cmd='星门')
@dft_blueprint.route('/speech',methods=['GET','POST'])
def Speech():
    listen_text = ''
    novelname = '吴迪专用在线朗读器'
    if request.method == 'POST':

        keyword = request.form.get('keyword')
        if keyword==None:
            # keyword = 'https://m.bbiquge.net/book/104535/57234049.html'
            # novel_name, title_name, listen_text, state = listen_data(keyword)
            return render_template('Speech.html', content_text=listen_text,novelname='请输入关键字',state='error')
        else:
            keyword=keyword
            novel_name, title_name, listen_text, state = listen_data(keyword)
            return render_template('Speech.html', content_text=listen_text, novelname='吴迪专用在线朗读器', state='normal')
    return render_template('Speech.html', content_text=listen_text, novelname=novelname, state='normal')
@dft_blueprint.route('/',methods=['GET','POST'])
def listen_home():
    url='https://m.bbiquge.net/book/104535/57234049.html'
    novel_name, title_name, listen_text,state = listen_data(url)
    title='小说听书页面'
    subtitle=title_name
    titlename=novel_name
    subtitlename=title_name

    # get_listen_text()

    return render_template('Home.html',subtitlename=subtitlename,titlename=titlename,title=title,subtitle=subtitle)
@dft_blueprint.route('/listen',methods=['GET','POST'])
def listen():
    state='error'

    if not os.path.exists(listen_dir):
        os.mkdir(listen_dir)
    if request.method == 'POST':

        keyword=request.form.get('keyword')


        if keyword==None:
            return render_template('run.html',novel_name='请输入关键字',state='error')
        else:
            keyword=keyword
            # keyword = 'https://m.bbiquge.net/book/104535/57234049.html'
            novel_name,title_name,listen_text,state=listen_data(keyword)
# novel_name,title_name,listen_text,state=listen_data(keyword)

            return render_template("run.html",state=state,novel_name=novel_name,title_name=title_name,listen_text=listen_text)
    return render_template("run.html",state=state)
