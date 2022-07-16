#!/usr/bin/python
# -*- coding: utf-8 _*_
'''
 @File     : repest.py
 @Time     : 2022/5/9 16:27
 @Software : PyCharm
 @Author   : Tom
 @Version  : 
'''

import os
import tkinter as tk
from tkinter import scrolledtext

import requests


class Appdate():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('百度翻译')
        self.root.geometry('300x200+500+100')
        self.root.resizable(False, False)
        self.value = tk.StringVar()
        self.value.set('请输入要翻译的内容:')
        button = tk.Button(self.root, text='翻译', command=self.translate)
        button.pack()
        self.entry = tk.Entry(self.root,textvariable=self.value)
        self.entry.pack()
        self.text=scrolledtext.ScrolledText(self.root,width=30,height=10)
        self.text.pack()
        self.root.mainloop()
    def translate(self):
        if self.value.get()=='请输入要翻译的内容:':
            self.value.set('')
        else:
            if self.value.get()=='':
                self.value.set('请输入要翻译的内容:')
            else:
                self.text.delete(0.0,tk.END)
                word = self.value.get()
                self.baidu_fanyi(word)
    def baidu_fanyi(self,word):
        url = 'https://fanyi.baidu.com/sug'
        data = {'kw': word} # 你只需要改kw对应的值
        res = requests.post(url, data=data).json()
        pt=res['data'][0]['v']
        self.text.insert(0.0,pt)
        # print(res['data'][0]['v'])
        # 输出: int. 打招呼; 哈喽，喂; 你好，您好; 表示问候 n. “喂”的招呼声或问候声 vi. 喊“喂

if __name__ == '__main__':
    Appdate()
