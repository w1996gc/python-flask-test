#!/usr/bin/python
# -*- coding: utf-8 _*_
'''
 @File     : listen_app.py
 @Time     : 2022/5/14 23:57
 @Software : PyCharm
 @Author   : Tom
 @Version  : 
'''

import os
from flask import Flask, render_template, request, jsonify

from Listen_novel_in_web import dft_blueprint

app=Flask(__name__)
app.register_blueprint(dft_blueprint)

app.run(host='0.0.0.0',port=5756,debug=True)
