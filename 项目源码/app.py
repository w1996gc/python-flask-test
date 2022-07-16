import random
import re

import pymysql
from flask import Flask as _Flask, jsonify, flash

from flask.json import JSONEncoder as _JSONEncoder
from jieba.analyse import extract_tags
import spider
import decimal
import utils
import string
import json
from hashlib import md5
import os
import platform
import pandas as pd
import requests
from bs4 import BeautifulSoup
from flask import Blueprint, render_template, request
from User_related import Application
from reposted import baidu_fanyi
import Conn


# def connecting_data():
#     conn = pymysql.connect(host='121.62.21.198', user='root', password='', db='test', charset='utf8')
#     cur = conn.cursor()
#     return cur,conn
class JSONEncoder(_JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        super(_JSONEncoder, self).default(o)


class Flask(_Flask):
    json_encoder = JSONEncoder


app = Flask(__name__)


# -------------前台页面相关服务接口start----------------
# 系统默认路径前台跳转
# 系统默认路径前台跳转
@app.route('/')
def main_page():
    return render_template("main.html")


# 获取服务器时间
@app.route('/time')
def get_time():
    return utils.get_time()


# 中间统计数据
@app.route('/c1')
def get_c1_data():
    data = utils.get_c1_data()
    return jsonify({"confirm": data[0], "suspect": data[1], "heal": data[2], "dead": data[3]})


# 中间地图统计数据
@app.route('/c2')
def get_c2_data():
    res = []
    for tup in utils.get_c2_data():
        res.append({"name": tup[0], "value": int(tup[1])})
    return jsonify({"data": res})


# 左上数据 累计确诊数据
@app.route('/l1')
def get_l1_data():
    data = utils.get_l1_data()
    day, confirm, suspect, heal, dead = [], [], [], [], []
    for a, b, c, d, e in data[7:]:
        day.append(a.strftime("%m-%d"))
        confirm.append(b)
        suspect.append(c)
        heal.append(d)
        dead.append(e)
    return jsonify({"day": day, "confirm": confirm, "suspect": suspect, "heal": heal, "dead": dead})


# 左下数据 新增确诊以及疑似
@app.route('/l2')
def get_l2_data():
    data = utils.get_l2_data()
    day, confirm_add, suspect_add = [], [], []
    for a, b, c in data[7:]:
        day.append(a.strftime("%m-%d"))
        confirm_add.append(b)
        suspect_add.append(c)
    return jsonify({"day": day, "confirm_add": confirm_add, "suspect_add": suspect_add})


# 右边上面数据 疫情确诊前5
@app.route('/r1')
def get_r1_data():
    data = utils.get_r1_data()
    city = []
    confirm = []
    for k, v in data:
        city.append(k)
        confirm.append(int(v))
    return jsonify({"city": city, "confirm": confirm})


# 右边下面数据 热点新闻词
@app.route('/r2')
def get_r2_data():
    data = utils.get_r2_data()
    d = []
    for i in data:
        k = i[0].rstrip(string.digits)
        v = i[0][len(k) - 1:]
        ks = extract_tags(k)
        for j in ks:
            if not j.isdigit():
                d.append({"name": j, "value": "111"})
    return jsonify({"kws": d})


# -------------前台页面相关服务接口end-----------------
## 登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not all([username, password]):
            flash('参数不完整')
        res = utils.get_user(username, password)
        # get_admin(username)
        if res:
            dd='200'
            user_dd(dd)
            return render_template('index.html')
        else:
            return render_template('login_error.html')
    return render_template('login.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=='POST':
        username=request.form.get('username')
        password = request.form.get('password')
        Phone_number=request.form.get('Phone_number')
        mail=request.form.get('mail')
        tel=re.match(r"^1[35678]\d{9}$",Phone_number)
        if not all([username, password,Phone_number,mail]):
            flash('参数不完整')
        if tel and '@' in mail:
            try:
                n = random.randint(1, 10)
                res=utils.get_register(n,username,password,mail,Phone_number)
                # get_admin(username)
                if res:
                    dd='200'
                    user_dd(dd)
                    return render_template('index.html')
                    # return render_template('html/welcome.html',admin=admin)
                else:
                    return render_template('login_error.html')
            except Exception as e:
                a = random.randint(1, 10)
                b = 1
                n = a + b + 1
                res=utils.get_register(n,username,password,mail,Phone_number)
                # get_admin(username)
                if res:
                    dd='200'
                    user_dd(dd)
                    return render_template('index.html')
                else:
                    return render_template('login_error.html')
    return render_template('register.html')
# 登录页面跳转
@app.route('/admin')
def admin():
    return render_template('login.html')


# 后台首页面跳转
@app.route('/html/welcome')
def welcome():
    return render_template('html/welcome.html',admin='Administrator')
@app.route('/getdate')
def get_admin():
    spider.update_history()
    spider.update_hotsearch()
    return render_template("main.html")

# 区域数据监测页面跳转
@app.route('/html/new')
def new():
    return render_template('html/new.html')


# 历史统计数据监测页面跳转
@app.route('/html/old')
def old():
    return render_template('html/old.html')


# 新闻标题数据监测页面跳转
@app.route('/html/news')
def news():
    return render_template('html/news.html')


# 获取分页历史统计数据
@app.route('/old/list', methods=["POST"])
def old_list():
    get_data = request.form.to_dict()
    page_size = get_data.get('page_size')
    page_no = get_data.get('page_no')
    param = get_data.get('param')
    data, count, page_list, max_page = utils.get_old_list(int(page_size), int(page_no), param)
    return jsonify({"data": data, "count": count, "page_no": page_no, "page_list": page_list, "max_page": max_page})


# 修改历史统计数据
@app.route('/old/edit', methods=["POST"])
def old_edit():
    get_data = request.form.to_dict()
    ds = get_data.get('ds')
    confirm = get_data.get('confirm')
    confirm_add = get_data.get('confirm_add')
    suspect = get_data.get('suspect')
    suspect_add = get_data.get('suspect_add')
    heal = get_data.get('heal')
    heal_add = get_data.get('heal_add')
    dead = get_data.get('dead')
    dead_add = get_data.get('dead_add')
    utils.edit_old(ds, confirm, confirm_add, suspect, suspect_add, heal, heal_add, dead, dead_add)
    return '200'

# 删除历史统计数据
@app.route('/old/del', methods=["DELETE"])
def old_del():
    get_data = request.form.to_dict()
    ds = get_data.get('ds')
    utils.del_old(ds)
    return '200'


# 获取分页区域统计数据
@app.route('/new/list', methods=["POST"])
def new_list():
    get_data = request.form.to_dict()
    page_size = get_data.get('page_size')
    page_no = get_data.get('page_no')
    param = get_data.get('param')
    data, count, page_list, max_page = utils.get_new_list(int(page_size), int(page_no), param)
    return jsonify({"data": data, "count": count, "page_no": page_no, "page_list": page_list, "max_page": max_page})


# 修改区域统计数据
@app.route('/new/edit', methods=["POST"])
def new_edit():
    get_data = request.form.to_dict()
    id = get_data.get('id')
    confirm = get_data.get('confirm')
    confirm_add = get_data.get('confirm_add')
    heal = get_data.get('heal')
    dead = get_data.get('dead')
    utils.edit_new(id, confirm, confirm_add, heal, dead)
    return '200'


# 删除区域统计数据
@app.route('/new/del', methods=["DELETE"])
def new_del():
    get_data = request.form.to_dict()
    id = get_data.get('id')
    utils.del_new(id)
    return '200'


# 获取分页新闻标题数据
@app.route('/news/list', methods=["POST"])
def news_list():
    get_data = request.form.to_dict()
    page_size = get_data.get('page_size')
    page_no = get_data.get('page_no')
    param = get_data.get('param')
    data, count, page_list, max_page = utils.get_news_list(int(page_size), int(page_no), param)
    return jsonify({"data": data, "count": count, "page_no": page_no, "page_list": page_list, "max_page": max_page})


# 修改新闻标题数据
@app.route('/news/edit', methods=["POST"])
def news_edit():
    get_data = request.form.to_dict()
    id = get_data.get('id')
    content = get_data.get('content')
    utils.edit_news(id, content)
    return '200'


# 删除新闻标题数据
@app.route('/news/del', methods=["DELETE"])
def news_del():
    get_data = request.form.to_dict()
    id = get_data.get('id')
    utils.del_news(id)
    return '200'


from concurrent.futures import ThreadPoolExecutor


# 后台调用爬虫
@app.route('/spider/start', methods=["POST"])
def online():
    executor = ThreadPoolExecutor(2)
    executor.submit(spider.online())
    return '200'
# 数据清空
@app.route('/data/clear', methods=['GET', 'POST'])
def data_clear():
    utils.get_data_clear()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not all([username, password]):
            flash('参数不完整')
        res = utils.get_user(username, password)
        # get_admin(username)
        if res:
            dd = '200'
            user_dd(dd)
            return render_template('index.html')
        else:
            return render_template('login_error.html')
    return render_template('login.html')
@app.route('/data/login', methods=['GET', 'POST'])
def data_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not all([username, password]):
            flash('参数不完整')
        res = utils.get_user(username, password)
        # get_admin(username)
        if res:
            dd='200'
            user_dd(dd)
            return render_template('index.html')
        else:
            return render_template('login_error.html')
    return render_template('login.html')

# -------------后台相关服务接口end-----------------
def user_dd(dd):
    global ddcc
    ddcc=dd
    return ddcc
# -------------mysql相关-----------------
@app.route('/create')
def create_db():
    createdb()
    return render_template('main.html')
@app.route('/sql/getdate')
def create_get_date():
    # utils.create_date()
    return render_template('appdata.html')
@app.route('/sql/adb')
def create_s1():
    conn = pymysql.connect(host="127.0.0.1", user="root", password="123456", db="mysql", charset="utf8")
    cur = conn.cursor()
    sql = f"create database `test`"
    cur.execute(sql)
    cur.close()
    conn.close()
    return render_template('数据库管理.html')
@app.route('/sql/sdb')
def create_sd1():
    conn = pymysql.connect(host="127.0.0.1", user="root", password="123456", db="mysql", charset="utf8")
    cur = conn.cursor()
    sql = f"show databases"
    cur.execute(sql)
    res = cur.fetchall()
    labels = [l[0] for l in res]
    cur.close()
    conn.close()
    return render_template('数据库管理.html', labels=labels)
@app.route('/sql/数据库管理.html')
def create_c2():
    return render_template('数据库管理.html')
@app.route('/sql/数据表管理.html')
def create_s2():
    return render_template('数据表管理.html')
@app.route('/sql/add_data.html')
def create_s3():
    return render_template('add_data.html')
@app.route('/sql/details')
def create_tab1():
    cur, conn=Conn.conn()
    sql=f"CREATE TABLE `test`.`details`  (`id` int NOT NULL AUTO_INCREMENT,`update_time` datetime NULL DEFAULT NULL COMMENT '数据最后更新时间',`province` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '省',`city` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '市',`confirm` int NULL DEFAULT NULL COMMENT '累计确诊',`confirm_add` int NULL DEFAULT NULL COMMENT '新增治愈',`heal` int NULL DEFAULT NULL COMMENT '累计治愈',`dead` int NULL DEFAULT NULL COMMENT '累计死亡',PRIMARY KEY (`id`) USING BTREE) ENGINE = InnoDB AUTO_INCREMENT = 552 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;"
    cur.execute(sql)
    cur.close()
    conn.close()
    return render_template('add_data.html')
@app.route('/sql/history')
def create_tab2():
    cur, conn=Conn.conn()
    sql=f"CREATE TABLE `test`.`history`  (`ds` datetime NOT NULL COMMENT '日期',`confirm` int NULL DEFAULT NULL COMMENT '累计确诊',`confirm_add` int NULL DEFAULT NULL COMMENT '当日新增确诊',`suspect` int NULL DEFAULT NULL COMMENT '剩余疑似',`suspect_add` int NULL DEFAULT NULL COMMENT '当日新增疑似',`heal` int NULL DEFAULT NULL COMMENT '累计治愈',`heal_add` int NULL DEFAULT NULL COMMENT '当日新增治愈',`dead` int NULL DEFAULT NULL COMMENT '累计死亡',`dead_add` int NULL DEFAULT NULL COMMENT '当日新增死亡',PRIMARY KEY (`ds`) USING BTREE) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;"
    cur.execute(sql)
    cur.close()
    conn.close()
    return render_template('add_data.html')
@app.route('/sql/hotsearch')
def create_tab3():
    cur, conn=Conn.conn()
    sql=f"CREATE TABLE `test`.`hotsearch`  (`id` int NOT NULL AUTO_INCREMENT,`dt` datetime NULL DEFAULT NULL,`content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,PRIMARY KEY (`id`) USING BTREE) ENGINE = InnoDB AUTO_INCREMENT = 61 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;"
    cur.execute(sql)
    cur.close()
    conn.close()
    return render_template('add_data.html')
@app.route('/sql/sys_user')
def create_tab4():
    cur, conn=Conn.conn()
    sql=f"CREATE TABLE `sys_user`  (`id` int NOT NULL AUTO_INCREMENT,`username` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,`password` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,`name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,`email` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,`phone` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,PRIMARY KEY (`id`) USING BTREE) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;"
    cur.execute(sql)
    cur.close()
    conn.close()
    return render_template('add_data.html')
@app.route('/sql/thyssenkrupp')
def create_tab5():
    cur, conn=Conn.conn()
    sql=f"CREATE TABLE `thyssenkrupp` (`错误码` varchar(60) COLLATE utf8mb4_bin NOT NULL DEFAULT '',`错误说明` varchar(100) COLLATE utf8mb4_bin NOT NULL DEFAULT '',`原因及修理指南` varchar(200) COLLATE utf8mb4_bin DEFAULT NULL,`备注` varchar(25) COLLATE utf8mb4_bin DEFAULT NULL,PRIMARY KEY (`错误码`,`错误说明`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;"
    cur.execute(sql)
    cur.close()
    conn.close()
    return render_template('add_data.html')
@app.route('/sql/hitachi_mca')
def create_tab6():
    cur, conn=Conn.conn()
    sql=f"CREATE TABLE `hitachi_mca` (`TCD` varchar(30) NOT NULL,`host_department` varchar(60) DEFAULT NULL,`vice_department` varchar(60) DEFAULT NULL,PRIMARY KEY (`TCD`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;"
    cur.execute(sql)
    cur.close()
    conn.close()
    return render_template('add_data.html')
# -------------用户相关-----------------
# 忘记密码
@app.route('/forgot')
def forgot_password():
    return '200'
@app.route('/user/revise')
def UserRevise():
    Application()
    return '请到UI界面修改!'
# 查看用户
# @app.route('/account/user_list',methods='POST')
# def user_list():
#     get_data=request.form.to_dict()
#     print(get_data)
#     page_size = get_data.get('page_size')
#     page_no = get_data.get('page_no')
#     param = get_data.get('param')
#     print(page_size,page_no,param)
#     data, count, page_list, max_page = utils.get_user_list(int(page_size), int(page_no), param)
#     print(jsonify({"data": data, "count": count,"page_list":page_list,"max_page":max_page}))
#     return jsonify({"data": data, "count": count,"page_list":page_list,"max_page":max_page})

@app.route('/display')
def user_account():
    return render_template('admin.html')
@app.route('/account')
def User_display():
    try:
        dd = user_dd(ddcc)
        if dd:
            # conn = pymysql.connect(host='121.62.21.198',user='root',password='',db='test',charset='utf8')
            # cur = conn.cursor()
            cur,conn = Conn.conn()

            sql = "select * from sys_user"
            cur.execute(sql)
            content = cur.fetchall()

            # 获取表头
            sql = "SHOW FIELDS FROM sys_user"
            cur.execute(sql)
            labels = cur.fetchall()
            labels = [l[0] for l in labels]

            return render_template('admin.html', labels=labels, content=content)
    except Exception as ee:
        if '1049' in ee:
            createdb()
        return render_template('login.html')

# -------------电梯翻译相关-----------------




@app.route('/download', methods=['GET', 'POST'])
def package_download():
    if request.method == 'POST':

        key = request.form.get('keypackage')
        result, appdate = pypi_download(key)
        keyurl = request.form.get('keyurl')
        if keyurl != None:
            resultt, appdated = url_download(keyurl)
            return render_template("demo/download.html", resultt=resultt, appdated=appdated)
        return render_template("demo/download.html", result=result, appdate=appdate)
    elif request.method == 'GET':
        return render_template("demo/download.html")


@app.route('/日立', methods=['GET', 'POST'])
def Hitachi_mca():
    result = ''
    errill = ''
    errreason = ''
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        # errill, errreason = get_mca_conn(keyword)
        if keyword == '0000':
            labels, content = mca()
            datatext = getmca()
            # print(datatext)
            return render_template('demo/mca.html', datatext=datatext, labels=labels, content=content, result=keyword)
        errill, errreason = get_mca_conn(keyword)
        return render_template('demo/mca.html', errill=errill, result=keyword, errreason=errreason)
    return render_template('demo/mca.html', errill=errill, result=result, errreason=errreason)


@app.route('/迅达', methods=['GET', 'POST'])
def left_all():
    result = ''
    errill = ''
    errreason = ''
    datatext = getconn()
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        if keyword == '0000':
            return render_template('demo/Schindler.html', errill=errill, result=keyword, errreason=errreason,
                                   datatext=datatext)
    return render_template('demo/Schindler.html', errill=errill, result=result, errreason=errreason)


@app.route('/蒂森', methods=['GET', 'POST'])
def left():
    result = ''
    errill = ''
    errreason = ''
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        errill, errreason = get_conn(keyword)
        if keyword == '0000':
            datatext = getconn()
            print(datatext)
            return render_template('demo/left.html', result=keyword, datatext=datatext)
        return render_template('demo/left.html', errill=errill, result=keyword, errreason=errreason)
    return render_template('demo/left.html', errill=errill, result=result, errreason=errreason)


@app.route('/left', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        key = request.form.get('myselect')
        if key == '蒂森':
            return render_template('demo/index.html', key=key)
        elif key == '迅达':
            return render_template('demo/index.html', key=key)
        elif key == '日立':
            return render_template('demo/index.html', key=key)
        else:
            left = ''
            return render_template("demo/index.html", key=left)
    else:
        left = ''
        return render_template("demo/index.html", key=left)
    # return render_template("index.html")


@app.route('/zh', methods=['GET', 'POST'])
def Chinese_to_English():
    result = "查询结果"
    appdate = ""
    from_lang = 'zh'
    to_lang = 'en'
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        if keyword == "":
            appdate = "请输入要翻译的内容"
        else:
            date = BaiduFanyi(from_lang, to_lang, keyword)
            target = date_to_str(date)
            appdate = "翻译《{}》成功,结果为:\n{}".format(keyword, target)
    return render_template("demo/zh.html", result=result, appdate=appdate)


@app.route('/eg', methods=['GET', 'POST'])
def English_to_Chinese():
    result = "查询结果"
    appdate = ""
    from_lang = 'en'
    to_lang = 'zh'
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        if keyword == "":
            appdate = "请输入要翻译的内容"
        else:
            date = BaiduFanyi(from_lang, to_lang, keyword)
            target = date_to_str(date)
            appdate = "翻译{}成功,结果为:\n{}".format(keyword, target)
    return render_template("demo/eg.html", result=result, appdate=appdate)


@app.route('/main', methods=['GET', 'POST'])
def main():
    result = "查询结果"
    appdate = ""
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        if keyword == "":
            appdate = "请输入要翻译的内容"
        else:
            appdate = baidu_fanyi(keyword)

    return render_template("demo/main.html", result=result, appdate=appdate)


@app.errorhandler(404)
def error_date(error):
    return render_template("demo/404.html", error=error), 404


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
        pst = v['dst']
        return str(pst)


def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()


def mca():
    # conn = pymysql.connect(host='121.62.21.198', user='root', password='', db='test', charset='utf8')
    # cur = conn.cursor()
    cur,conn = Conn.conn()
    sql = "select * from hitachi_mca"
    cur.execute(sql)
    content = cur.fetchall()

    # 获取表头
    sql = "SHOW FIELDS FROM hitachi_mca"
    cur.execute(sql)
    labels = cur.fetchall()
    labels = [l[0] for l in labels]

    return labels, content


def get_conn(sql):
    try:
        # conn = pymysql.connect(host='121.62.21.198', user='root', password='', db='test', port=3306, charset='utf8')
        # cur = conn.cursor()
        cur,conn = Conn.conn()
        sql = f"select * from `test`.`thyssenkrupp` where 错误码 = '{sql}'"
        cur.execute(sql)
        data = cur.fetchall()
        errill = data[0][1]
        errreason = data[0][2]
        cur.close()
        conn.close()
        if errreason == '':
            errreason = '暂无'
            return errill, errreason
        return errill, errreason
    except Exception as ee:
        e = '该故障代码不存在，请检查后重新输入'
        if '1049' in ee:
            createdb()
        return 'Error:{}——{}'.format(e, ee), '程序出错'
    except TimeoutError as err:
        return 'Error:{}'.format(err), '程序超时'


def getconn():
    text_connent = '蒂森故障表'
    return text_connent


def getmca():
    text_connent = '日立mca电梯故障'
    return text_connent


def get_mca_conn(sql):
    try:
        # conn = pymysql.connect(host='121.62.21.198', user='root', password='', db='test', port=3306, charset='utf8')
        # cur = conn.cursor()
        cur, conn = Conn.conn()
        sql = f"select * from `test`.`hitachi_mca` where TCD= '{sql}'"
        cur.execute(sql)
        data = cur.fetchall()
        errill = data[0][1]
        errreason = data[0][2]
        cur.close()
        conn.close()
        if errreason == '':
            errreason = '暂无'
            return errill, errreason
        return errill, errreason
    except Exception as ee:
        e = '该故障代码不存在，请检查后重新输入'
        if '1049' in ee:
            pass# createdb()
        return 'Error:{}——{}'.format(e, ee), '程序出错'
    except TimeoutError as err:
        return 'Error:{}'.format(err), '程序超时'


def getconn_data():
    try:
        # conn = pymysql.connect(host='121.62.21.198', user='root', password='', db='test', port=3306, charset='utf8')
        # cur = conn.cursor()
        cur, conn = Conn.conn()
        sql = "select * from `test`.`thyssenkrupp`"
        cur.execute(sql)
        data = cur.fetchall()
        cur.close()
        conn.close()
        return [var for var in data]
    except Exception as ee:
        if '1049' in ee:
            createdb()
        data = None
        return data


def pypi_download(package_name):
    if platform.system().lower() == 'windows':
        os.system('start D:\\Users\\Administrator\\OneDrive\\Desktop\\"Internet Download Manager.lnk"')
    elif platform.system().lower() == 'linux':
        pass
    # package_name = ''#package_entry.get()
    if package_name == None:
        return '请输入要下载的包名', '程序出错'
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
            return 'Error:{}'.format(ee), '下载失败'


def url_download(url):
    if platform.system().lower() == 'windows':
        os.system('start D:\\Users\\Administrator\\OneDrive\\Desktop\\"Internet Download Manager.lnk"')
    elif platform.system().lower() == 'linux':
        pass
    # url = ''#self.url_entry.get()
    try:
        cmd = 'idman /d {} /q /h /n'.format(url)

        os.system(cmd)
        return url, '下载完成'
    except Exception as ee:
        return 'Error:{}'.format(ee), '下载失败'
def createdb():
    try:
        # conn = pymysql.connect(host='121.62.21.198', user='root', password='', db='mysql', port=3306, charset='utf8')
        # cur = conn.cursor()
        cur, conn = Conn.conn()
        sql = "create database test"
        cur.execute(sql)
        cur.close()
        conn.close()
    except Exception as ee:
        if '1049' in ee:
            createdb()
        data = None
        return data

# -------------娱乐相关-----------------
@app.route('/chess')
def chinese_chess():
    return render_template("chess.html")

if __name__ == '__main__':
    # 端口号设置
    app.run(host="0.0.0.0", port=5672,debug=True)
