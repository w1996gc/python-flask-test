#!/usr/bin/python
# -*- coding: utf-8 _*_
'''
 @File     : app.py
 @Time     : 2022/5/9 12:53
 @Software : PyCharm
 @Author   : Tom
 @Version  : 
'''

import os
from flask import Flask, render_template, request, jsonify

from app_data import dft_blueprint

app=Flask(__name__)
app.register_blueprint(dft_blueprint)

app.run(host='0.0.0.0',debug=True)
