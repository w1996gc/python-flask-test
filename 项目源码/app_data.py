#!/usr/bin/python
# -*- coding: utf-8 _*_
'''
 @File     : app_data.py
 @Time     : 2022/5/8 23:18
 @Software : PyCharm
 @Author   : Tom
 @Version  : 
'''
import json
import random
from hashlib import md5
import os
import platform
import pandas as pd
import pymysql
import requests
from bs4 import BeautifulSoup
from flask import Blueprint, render_template, request
from reposted import baidu_fanyi
import Conn

dft_blueprint = Blueprint('default', __name__)

@dft_blueprint.route('/download',methods=['GET','POST'])
def package_download():
    if request.method=='POST':

        key=request.form.get('keypackage')
        result,appdate=package_download(key)
        keyurl=request.form.get('keyurl')
        if keyurl !=None:
            resultt,appdated=url_download(keyurl)
            return render_template("download.html",resultt=resultt,appdated=appdated)
        return render_template("download.html",result=result,appdate=appdate)
    elif request.method=='GET':
        return render_template("download.html")

@dft_blueprint.route('/日立',methods=['GET','POST'])
def Hitachi_mca():
    result=''
    errill=''
    errreason=''
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        errill, errreason = get_mca_conn(keyword)
        if keyword == '0000':
            labels,content = mca()
            datatext=getmca()
            # print(datatext)
            return render_template('mca.html',datatext=datatext,labels=labels, content=content,result=keyword)
        return render_template('mca.html',errill=errill,result=keyword,errreason=errreason)
    return render_template('mca.html',errill=errill,result=result,errreason=errreason)
@dft_blueprint.route('/迅达',methods=['GET','POST'])
def left_all():
    result=''
    errill=''
    errreason=''
    datatext = getconn()
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        if keyword=='0000':

            return render_template('Schindler.html',errill=errill,result=keyword,errreason=errreason,datatext=datatext)
    return render_template('Schindler.html',errill=errill,result=result,errreason=errreason)

@dft_blueprint.route('/蒂森',methods=['GET','POST'])
def left():
    result=''
    errill=''
    errreason=''
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        errill, errreason = get_conn(keyword)
        if keyword == '0000':
            datatext = getconn()
            print(datatext)
            return render_template('left.html',result=keyword,datatext=datatext)
        return render_template('left.html',errill=errill,result=keyword,errreason=errreason)
    return render_template('left.html',errill=errill,result=result,errreason=errreason)
@dft_blueprint.route('/',methods=['GET','POST'])
def index():
    if request.method=='POST':
        key=request.form.get('myselect')
        if key=='蒂森':
            return render_template('index.html',key=key)
        elif key=='迅达':
            return render_template('index.html',key=key)
        elif key=='日立':
            return render_template('index.html',key=key)
        else:
            left = ''
            return render_template("index.html",key=left)
    else:
        left=''
        return render_template("index.html",key=left)
    # return render_template("index.html")
@dft_blueprint.route('/zh',methods=['GET','POST'])
def Chinese_to_English():
    result="查询结果"
    appdate = ""
    from_lang = 'zh'
    to_lang = 'en'
    if request.method == 'POST':
       keyword= request.form.get('keyword')
       if keyword=="":
           appdate="请输入要翻译的内容"
       else:
           date = BaiduFanyi(from_lang, to_lang, keyword)
           target=date_to_str(date)
           appdate="翻译《{}》成功,结果为:\n{}".format(keyword,target)
    return render_template("zh.html",result=result,appdate=appdate)
@dft_blueprint.route('/eg',methods=['GET','POST'])
def English_to_Chinese():
    result="查询结果"
    appdate = ""
    from_lang = 'en'
    to_lang = 'zh'
    if request.method == 'POST':
       keyword= request.form.get('keyword')
       if keyword=="":
           appdate="请输入要翻译的内容"
       else:
           date = BaiduFanyi(from_lang, to_lang, keyword)
           target=date_to_str(date)
           appdate="翻译{}成功,结果为:\n{}".format(keyword,target)
    return render_template("eg.html",result=result,appdate=appdate)

@dft_blueprint.route('/main',methods=['GET','POST'])
def main():
    result="查询结果"
    appdate = ""
    if request.method == 'POST':
       keyword= request.form.get('keyword')
       if keyword=="":
          appdate="请输入要翻译的内容"
       else:
          appdate=baidu_fanyi(keyword)


    return render_template("main.html",result=result,appdate=appdate)


@dft_blueprint.errorhandler(404)
def error_date(error):
    return render_template("404.html",error=error),404

def BaiduFanyi(from_lang, to_lang, query):
    appid = '20220509001209410'
    appkey = 'rhQuJj1eugskVi3eGKsw'
    from_lang = from_lang
    to_lang = to_lang
    endpoint = 'http://api.fanyi.baidu.com'
    path = '/api/trans/vip/translate'
    url = endpoint + path
    salt = random.randint(32768, 65536)
    sign = make_md5(appid + query + str(salt) + appkey)
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()
    pt = json.dumps(result, indent=4, ensure_ascii=False)
    pt = json.loads(pt)
    date_to_str(pt)
    return pt


def date_to_str(pt):
    pnt = pt['trans_result']
    for v in pnt:
        pst=v['dst']
        return str(pst)
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


def mca():
    # conn = pymysql.connect(host='121.62.21.198', user='root', password='', db='test', charset='utf8')
    # cur = conn.cursor()
    cur, conn = Conn.conn()
    sql = "select * from hitachi_mca"
    cur.execute(sql)
    content = cur.fetchall()

    # 获取表头
    sql = "SHOW FIELDS FROM hitachi_mca"
    cur.execute(sql)
    labels = cur.fetchall()
    labels = [l[0] for l in labels]

    return labels,content


def get_conn(sql):
    try:
        # conn=pymysql.connect(host='121.62.21.198',user='root',password='',db='test',port=3306,charset='utf8')
        # cur=conn.cursor()
        cur, conn = Conn.conn()
        sql=f"select * from `test`.`thyssenkrupp` where 错误码 = '{sql}'"
        cur.execute(sql)
        data=cur.fetchall()
        errill=data[0][1]
        errreason=data[0][2]
        cur.close()
        conn.close()
        if errreason=='':
            errreason = '暂无'
            return errill,errreason
        return errill,errreason
    except Exception as ee:
        e='该故障代码不存在，请检查后重新输入'
        return 'Error:{}——{}'.format(e,ee),'程序出错'
    except TimeoutError as err:
        return 'Error:{}'.format(err),'程序超时'
def getconn():
    text_connent='蒂森故障表'
    return text_connent
def getmca():
    text_connent='日立mca电梯故障'
    return text_connent
def get_mca_conn(sql):
    try:
        # conn=pymysql.connect(host='121.62.21.198',user='root',password='',db='test',port=3306,charset='utf8')
        # cur=conn.cursor()
        cur, conn = Conn.conn()
        sql=f"select * from `test`.`hitachi_mca` where TCD= '{sql}'"
        cur.execute(sql)
        data=cur.fetchall()
        errill=data[0][1]
        errreason=data[0][2]
        cur.close()
        conn.close()
        if errreason=='':
            errreason = '暂无'
            return errill,errreason
        return errill,errreason
    except Exception as ee:
        e='该故障代码不存在，请检查后重新输入'
        return 'Error:{}——{}'.format(e,ee),'程序出错'
    except TimeoutError as err:
        return 'Error:{}'.format(err),'程序超时'
def getconn_data():
    try:
        # conn=pymysql.connect(host='121.62.21.198',user='root',password='',db='test',port=3306,charset='utf8')
        # cur=conn.cursor()
        cur, conn = Conn.conn()
        sql="select * from `test`.`thyssenkrupp`"
        cur.execute(sql)
        data=cur.fetchall()
        cur.close()
        conn.close()
        return [var for var in data]
    except Exception as ee:
        data=None
        return data

def package_download(package_name):
    if platform.system().lower()=='windows':
        os.system('start D:\\Users\\Administrator\\OneDrive\\Desktop\\"Internet Download Manager.lnk"')
    elif platform.system().lower()=='linux':
        pass
    # package_name = ''#package_entry.get()
    if package_name==None:
        return '请输入要下载的包名','程序出错'
    else:
        try:
            url = 'https://pypi.org/project/{}/#files'.format(package_name)
            resp = requests.get(url)
            resp.encoding = 'utf-8'
            soup = BeautifulSoup(resp.text, 'html.parser')

            company_item = soup.find_all('a')
            links = []
            for links in company_item:
                link = links.get('href')
                if link and 'https://files.pythonhosted.org/packages/' in link:
                    cmd = 'idman /d {} /q /h /n'.format(link)
                    os.system(cmd)
                    return link, '下载完成'
        except Exception as ee:
            return 'Error:{}'.format(ee),'下载失败'

def url_download(url):
    if platform.system().lower()=='windows':
        os.system('start D:\\Users\\Administrator\\OneDrive\\Desktop\\"Internet Download Manager.lnk"')
    elif platform.system().lower()=='linux':
        pass
    # url = ''#self.url_entry.get()
    try:
        cmd = 'idman /d {} /q /h /n'.format(url)

        os.system(cmd)
        return url, '下载完成'
    except Exception as ee:
        return 'Error:{}'.format(ee),'下载失败'

