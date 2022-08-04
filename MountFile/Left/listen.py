#!/usr/bin/python
# -*- coding: utf-8 _*_
'''
 @File     : listen.py
 @Time     : 2022/4/11 12:59
 @Software : PyCharm
 @Author   : Tom
 @Version  : 
'''

import os

import speech_recognition as sr

r=sr.Recognizer()
text=sr.AudioFile(r"D:\Program\Lib\site-packages\pygame\examples\data\whiff.wav")
with text as source:
    audio=r.record(source)
type(audio)
c=r.recognize_google(audio,language="zh-CN+en")
print(c)




