# -*- coding:utf-8 -*-

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

@app.route('/about.html',methods=['GET','POST'])
def data_about():
    return render_template('html/about.html')
# 获取服务器时间

@app.route('/music', methods=['GET',"POST"])
def py_music():
    pl_dir = './static/dict'
    pl_files = [file for file in os.listdir(pl_dir) if file.endswith('.py')]
    result="<meta name='viewport' content='width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no'><style>h3,a{font-size:50px;},.main{display: flex;flex-direction: column;}</style>"
    result+=f"""<h3>资源展示<br/><a href='/index.html'>Select Data</a></h3>"""
    for item in pl_files:
        result += f"<div class='main' style='display: flex;flex-direction: column;height: auto;margin: 10px auto;overflow: hidden;'>当前资源为:{item}<br/><a href='/static/dict/{item}'>{item}</a></div><br/>"
        # return render_template('image.html', result=os.path.join(image_dir,item))
    return result
@app.route('/time')
def get_time():
    return utils.get_time()
#  获取图片
@app.route('/image', methods=['GET',"POST"])
def webim():
    image_dir='./static/img'
    image_files = [file for file in os.listdir(image_dir) if file.endswith('.png')]
    image_file = request.args.get('image_file')
    result="<meta name='viewport' content='width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no'>"
    result+=f"""<h3>播放图片<br/><a href='/index.html'>Select Data</a><br/><br/><a href='/setimg'>Select Img</a></h3>"""
    index=0
    for item in image_files:
        index +=1
        result += f"<div class='main' style='display: flex;flex-direction: column;height: auto;margin: 5px auto;overflow: hidden;'>当前图片为第{index}张:{item}<br/><img src='/static/img/{item}'></a></div><br/>"
        # return render_template('image.html', result=os.path.join(image_dir,item))
    return result

@app.route('/setimg', methods=['GET',"POST"])
def select_img():
    return render_template('html/select_img.html')


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

def __register():
    data = {
        "host": "111.173.83.23",
        "user": "root",
        "password": "Wqq@123456",
        "db": "test",
        "charset": "utf8"
    }
    if not os.path.exists("auto.json"):
        json_str = json.dumps(data, indent=4)
        with open("auto.json", "w") as f:
            f.write(json_str)
    else:
        file = open('auto.json', 'rb')
        jsonData = json.load(file)
        host = jsonData['host']
        user = jsonData['user']
        pwd = jsonData['password']
        db = jsonData['db']
        charset = jsonData['charset']
        conn = pymysql.connect(host=host, user=user, password=pwd, db=db, charset=charset)
        cur = conn.cursor()

        sql=f"select count(*) from sys_user;"
        cur.execute(sql)
        content = cur.fetchall()
        n=str([i[0]for i in content])
        n=n.replace('[','')
        n=n.replace(']','')
        cur.close()
        conn.close()
        return n
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method=='POST':
        username=request.form.get('username')
        password = request.form.get('password')
        Phone_number=request.form.get('Phone_number')
        mail=request.form.get('mail')
        tel=re.match(r"^1[35678]\d{9}$",Phone_number)
        n=int(__register())
        if not all([username, password,Phone_number,mail]):
            flash('参数不完整')
        if tel and '@' in mail:
            n +=1
            try:
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
    data = {
        "host": "111.173.83.23",
        "user": "root",
        "password": "Wqq@123456",
        "db": "test",
        "charset": "utf8"
    }
    if not os.path.exists("auto.json"):
        json_str = json.dumps(data, indent=4)
        with open("auto.json", "w") as f:
            f.write(json_str)
    else:
        file = open('auto.json', 'rb')
        jsonData = json.load(file)
        host = jsonData['host']
        user = jsonData['user']
        pwd = jsonData['password']
        db = jsonData['db']
        charset = jsonData['charset']
        conn = pymysql.connect(host=host, user=user, password=pwd, db=db, charset=charset)
        cur = conn.cursor()
        sql = f"create database `test`"
        cur.execute(sql)
        cur.close()
        conn.close()
        return render_template('数据库管理.html')
@app.route('/sql/sdb')
def create_sd1():
    data = {
        "host": "111.173.83.23",
        "user": "root",
        "password": "Wqq@123456",
        "db": "test",
        "charset": "utf8"
    }
    if not os.path.exists("auto.json"):
        json_str = json.dumps(data, indent=4)
        with open("auto.json", "w") as f:
            f.write(json_str)
    else:
        file = open('auto.json', 'rb')
        jsonData = json.load(file)
        host = jsonData['host']
        user = jsonData['user']
        pwd = jsonData['password']
        db = jsonData['db']
        charset = jsonData['charset']
        conn = pymysql.connect(host=host, user=user, password=pwd, db=db, charset=charset)
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
    sql=f"CREATE TABLE `sys_user`  (`id` int NOT NULL AUTO_INCREMENT,`username` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,`password` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,`name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,`email` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,`phone` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,PRIMARY KEY (`id`) USING BTREE) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;"
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
@app.route('/sql/creation')
def one_creation():
    cur, conn = Conn.conn()
    sql=f"CREATE TABLE `test`.`details`  (`id` int NOT NULL AUTO_INCREMENT,`update_time` datetime NULL DEFAULT NULL COMMENT '数据最后更新时间',`province` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '省',`city` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '市',`confirm` int NULL DEFAULT NULL COMMENT '累计确诊',`confirm_add` int NULL DEFAULT NULL COMMENT '新增治愈',`heal` int NULL DEFAULT NULL COMMENT '累计治愈',`dead` int NULL DEFAULT NULL COMMENT '累计死亡',PRIMARY KEY (`id`) USING BTREE) ENGINE = InnoDB AUTO_INCREMENT = 552 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;"
    cur.execute(sql)

    sql=f"CREATE TABLE `test`.`history`  (`ds` datetime NOT NULL COMMENT '日期',`confirm` int NULL DEFAULT NULL COMMENT '累计确诊',`confirm_add` int NULL DEFAULT NULL COMMENT '当日新增确诊',`suspect` int NULL DEFAULT NULL COMMENT '剩余疑似',`suspect_add` int NULL DEFAULT NULL COMMENT '当日新增疑似',`heal` int NULL DEFAULT NULL COMMENT '累计治愈',`heal_add` int NULL DEFAULT NULL COMMENT '当日新增治愈',`dead` int NULL DEFAULT NULL COMMENT '累计死亡',`dead_add` int NULL DEFAULT NULL COMMENT '当日新增死亡',PRIMARY KEY (`ds`) USING BTREE) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;"
    cur.execute(sql)

    sql=f"CREATE TABLE `test`.`hotsearch`  (`id` int NOT NULL AUTO_INCREMENT,`dt` datetime NULL DEFAULT NULL,`content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,PRIMARY KEY (`id`) USING BTREE) ENGINE = InnoDB AUTO_INCREMENT = 61 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;"
    cur.execute(sql)

    sql=f"CREATE TABLE `sys_user`  (`id` int NOT NULL AUTO_INCREMENT,`username` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,`password` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,`name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,`email` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,`phone` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,PRIMARY KEY (`id`) USING BTREE) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;"
    cur.execute(sql)

    sql=f"CREATE TABLE `thyssenkrupp` (`错误码` varchar(60) COLLATE utf8mb4_bin NOT NULL DEFAULT '',`错误说明` varchar(100) COLLATE utf8mb4_bin NOT NULL DEFAULT '',`原因及修理指南` varchar(200) COLLATE utf8mb4_bin DEFAULT NULL,`备注` varchar(25) COLLATE utf8mb4_bin DEFAULT NULL,PRIMARY KEY (`错误码`,`错误说明`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;"
    cur.execute(sql)

    sql=f"CREATE TABLE `hitachi_mca` (`TCD` varchar(30) NOT NULL,`host_department` varchar(60) DEFAULT NULL,`vice_department` varchar(60) DEFAULT NULL,PRIMARY KEY (`TCD`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;"
    cur.execute(sql)
    sql=f"create table `test`.`maintenance_plan`(`number` varchar(60) not null,`position` varchar(100) not null,`left1-半月` varchar(100) not null,`left2-半年` varchar(100) not null,`left3-半月` varchar(100) not null,`left4-半月` varchar(100),PRIMARY KEY (`number`,`position`,`left1-半月`,`left2-半年`,`left3-半月`,`left4-半月`))ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;"
    cur.execute(sql)
    cur.close()
    conn.close()
    return render_template('数据表管理.html')
@app.route('/spided', methods=['GET',"POST"])
def online_date():
    if request.method == 'POST':
        left=request.form.get('left')
        labels, content, sql = spider._my_online(left)
        return render_template('html/new_index.html', labels=labels, content=content, sql=sql)
    labels,content,sql = _get_sql()

    #labels, content, sql = spider.my_online()
    return render_template('html/new_index.html', labels=labels, content=content, sql=sql)

@app.route('/update.html',methods=['GET','POST'])
def my_update_date():
    if request.method == 'POST':
        number=request.form.get('number')
        new_number=request.form.get('new_number')
        left=request.form.get('left')
        labels,content,sql = get_my_sql(left,new_number, number)
        return render_template('html/update.html', labels=labels, content=content,sql=sql)
    labels,content,sql = _get_sql()
    return render_template('html/update.html', labels=labels, content=content,sql=sql)
def get_my_sql(left, new_number,number):
    try:
        data = {
            "host": "111.173.83.23",
            "user": "root",
            "password": "Wqq@123456",
            "db": "test",
            "charset": "utf8"
        }
        if not os.path.exists("auto.json"):
            json_str = json.dumps(data, indent=4)
            with open("auto.json", "w") as f:
                f.write(json_str)
        else:
            file = open('auto.json', 'rb')
            jsonData = json.load(file)
            host = jsonData['host']
            user = jsonData['user']
            pwd = jsonData['password']
            db = jsonData['db']
            charset = jsonData['charset']
            conn = pymysql.connect(host=host, user=user, password=pwd, db=db, charset=charset)
            cur = conn.cursor()
            #sql1 = "select `number`,`position`,`{}` from maintenance_plan where `{}`='{}' order by `number` desc".format(left,left, number)
            sql1="update maintenance_plan set `{}`='{}' where number='{}'".format(left,new_number,number)
            cur.execute(sql1)
            conn.commit()
            #content = cur.fetchall()
            sql2 = "select * from maintenance_plan order by `left1-半月` asc"
            cur.execute(sql2)
            content1 = cur.fetchall()

            # 获取表头
            sql = "SHOW FIELDS FROM maintenance_plan"
            cur.execute(sql)
            labels = cur.fetchall()
            labels = [l[0] for l in labels]
            cur.close()
            conn.close()

            return labels,content1,sql1
    except Exception as e:
        data = {
            "host": "111.173.83.23",
            "user": "root",
            "password": "Wqq@123456",
            "db": "test",
            "charset": "utf8"
        }
        if not os.path.exists("auto.json"):
            json_str = json.dumps(data, indent=4)
            with open("auto.json", "w") as f:
                f.write(json_str)
        else:
            file = open('auto.json', 'rb')
            jsonData = json.load(file)
            host = jsonData['host']
            user = jsonData['user']
            pwd = jsonData['password']
            db = jsonData['db']
            charset = jsonData['charset']
            conn = pymysql.connect(host=host, user=user, password=pwd, db=db, charset=charset)
            cur = conn.cursor()

            sql = "select * from maintenance_plan order by `left1-半月` asc"
            cur.execute(sql)

            content = cur.fetchall()

            # 获取表头
            sql = "SHOW FIELDS FROM maintenance_plan"
            cur.execute(sql)
            labels = cur.fetchall()
            labels = [l[0] for l in labels]
            cur.close()
            conn.close()

            return labels,content,e


@app.route('/index.html',methods=['GET','POST'])
def my_left():
    if request.method == 'POST':
        number=request.form.get('number')
        left=request.form.get('left')
        labels,content,sql = get_sql(left, number)
        return render_template('html/index.html', labels=labels, content=content,sql=sql)
    labels,content,sql = _get_sql()
    return render_template('html/index.html', labels=labels, content=content,sql=sql)
def _get_sql():
    data = {
        "host": "111.173.83.23",
        "user": "root",
        "password": "Wqq@123456",
        "db": "test",
        "charset": "utf8"
    }
    if not os.path.exists("auto.json"):
        json_str = json.dumps(data, indent=4)
        with open("auto.json", "w") as f:
            f.write(json_str)
    else:
        file = open('auto.json', 'rb')
        jsonData = json.load(file)
        host = jsonData['host']
        user = jsonData['user']
        pwd = jsonData['password']
        db = jsonData['db']
        charset = jsonData['charset']
        conn = pymysql.connect(host=host, user=user, password=pwd, db=db, charset=charset)
        cur = conn.cursor()

        sql1 = "select * from maintenance_plan order by `left1-半月` asc"
        cur.execute(sql1)
        content = cur.fetchall()

        # 获取表头
        sql = "SHOW FIELDS FROM maintenance_plan"
        cur.execute(sql)
        labels = cur.fetchall()
        labels = [l[0] for l in labels]
        cur.close()
        conn.close()

        return labels, content,sql1
def get_sql(left, number):
    try:
        data = {
            "host": "111.173.83.23",
            "user": "root",
            "password": "Wqq@123456",
            "db": "test",
            "charset": "utf8"
        }
        if not os.path.exists("auto.json"):
            json_str = json.dumps(data, indent=4)
            with open("auto.json", "w") as f:
                f.write(json_str)
        else:
            file = open('auto.json', 'rb')
            jsonData = json.load(file)
            host = jsonData['host']
            user = jsonData['user']
            pwd = jsonData['password']
            db = jsonData['db']
            charset = jsonData['charset']
            conn = pymysql.connect(host=host, user=user, password=pwd, db=db, charset=charset)
            cur = conn.cursor()

            sql1 = "select `number`,`position`,`{}` from maintenance_plan where `{}`='{}' order by `number` desc".format(left,left, number)
            cur.execute(sql1)
            content = cur.fetchall()

            # 获取表头
            sql = "SHOW FIELDS FROM maintenance_plan"
            cur.execute(sql)
            labels = cur.fetchall()
            labels = [l[0] for l in labels]
            cur.close()
            conn.close()

            return labels,content,sql1
    except Exception as e:
        data = {
            "host": "111.173.83.23",
            "user": "root",
            "password": "Wqq@123456",
            "db": "test",
            "charset": "utf8"
        }
        if not os.path.exists("auto.json"):
            json_str = json.dumps(data, indent=4)
            with open("auto.json", "w") as f:
                f.write(json_str)
        else:
            file = open('auto.json', 'rb')
            jsonData = json.load(file)
            host = jsonData['host']
            user = jsonData['user']
            pwd = jsonData['password']
            db = jsonData['db']
            charset = jsonData['charset']
            conn = pymysql.connect(host=host, user=user, password=pwd, db=db, charset=charset)
            cur = conn.cursor()

            sql = "select * from maintenance_plan order by `left1-半月` asc"
            cur.execute(sql)
            content = cur.fetchall()

            # 获取表头
            sql = "SHOW FIELDS FROM maintenance_plan"
            cur.execute(sql)
            labels = cur.fetchall()
            labels = [l[0] for l in labels]
            cur.close()
            conn.close()

            return labels,content,e
# -------------mysql查询-----------------
@app.route('/sql/show/details')
def show_tab1():
    cur, conn=Conn.conn()
    sql=f"SELECT * FROM `test`.`details`"
    cur.execute(sql)
    content=cur.fetchall()
    # 获取表头
    sql = "SHOW FIELDS FROM details"
    cur.execute(sql)
    labels = cur.fetchall()
    labels = [l[0] for l in labels]
    cur.close()
    conn.close()
    return render_template('add_data.html',labels=labels, content=content)
@app.route('/sql/show/history')
def show_tab2():
    cur, conn=Conn.conn()
    sql=f"SELECT * FROM `test`.`history`"
    cur.execute(sql)
    content=cur.fetchall()
    # 获取表头
    sql = "SHOW FIELDS FROM history"
    cur.execute(sql)
    labels = cur.fetchall()
    labels = [l[0] for l in labels]
    cur.close()
    conn.close()
    return render_template('add_data.html',labels=labels, content=content)
@app.route('/sql/show/hotsearch')
def show_tab3():
    cur, conn=Conn.conn()
    sql=f"SELECT * FROM `test`.`hotsearch`"
    cur.execute(sql)
    content=cur.fetchall()
    # 获取表头
    sql = "SHOW FIELDS FROM hotsearch"
    cur.execute(sql)
    labels = cur.fetchall()
    labels = [l[0] for l in labels]
    cur.close()
    conn.close()
    return render_template('add_data.html',labels=labels, content=content)
@app.route('/sql/show/thyssenkrupp')
def show_tab4():
    cur, conn=Conn.conn()
    sql=f"SELECT * FROM `test`.`thyssenkrupp`"
    cur.execute(sql)
    content=cur.fetchall()
    # 获取表头
    sql = "SHOW FIELDS FROM thyssenkrupp"
    cur.execute(sql)
    labels = cur.fetchall()
    labels = [l[0] for l in labels]
    cur.close()
    conn.close()
    return render_template('add_data.html',labels=labels, content=content)
@app.route('/sql/show/hitachi_mca')
def show_tab5():
    cur, conn=Conn.conn()
    sql=f"SELECT * FROM `test`.`hitachi_mca`"
    cur.execute(sql)
    content=cur.fetchall()
    # 获取表头
    sql = "SHOW FIELDS FROM hitachi_mca"
    cur.execute(sql)
    labels = cur.fetchall()
    labels = [l[0] for l in labels]
    cur.close()
    conn.close()
    return render_template('add_data.html',labels=labels, content=content)
@app.route('/sql/account')
def show_tab6():

    # conn = pymysql.connect(host='111.173.83.23',user='root',password='Wqq@123456',db='test',charset='utf8')
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

    return render_template('add_data.html', labels=labels, content=content)
# -------------mysql插入-----------------
@app.route('/sql/insert/thyssenkrupp')
def insert_tab1():
    cur, conn=Conn.conn()
    sql=f"INSERT INTO `thyssenkrupp` VALUES ('01XX','停楼 XX 的 RK 或 RKD 未接通','检查停楼 XX 的 RK 接点或机械部分','6'),('0201','禁止叫车经由监视程序','CPU 上一只 8K-RAM 被命令指示','1'),('0202','类似 ZSE 在特殊程序被释放，仅 SiemensCPU','使用包含电池组 RAM 芯片的 Thyssen CPU（位置记忆如果发生电源异常或 HS 关闭）','1'),('0203','TCM 控制',' 8K-RAM 无法认定；F800 伴随发生','1'),('0204','TCM 控制',' 8K-EPROM 无法认定；F800 伴随发生','1'),('0280','不明确或错误操作状态','','1'),('0301','特殊程序中未规定恰当的隔离停楼','隔离停楼未定义（检查数据页）或错误的特殊程序 EPROM','1'),('0302','特殊程序中未规定恰当的停靠停楼','停靠停楼未定义（检查数据页）或错误的特殊程序 EPROM',''),('0303','特殊程序中未规定恰当的火警停靠停楼','火警停靠停楼未定义（检查数据页）或错误的特殊程序 EPROM',''),('04NN','TCI：磁簧开关 ZSE 引起的错误','一个以上的 ZSE 开关导通，电梯将被停止，错误码 04NN 连续纪录 4 次。检查 ZSE 开关','SM3'),('04XX','TCM：磁簧开关 ZSE 引起的错误','一个以上的 ZSE 开关导通，所有激磁的停楼ZSE 将被显示。检查 ZSE 开关',''),('0542','群控的电梯数或停楼数不可接受','',''),('0553','传输运转在错误的群控状态；05XX 随后发生','缺乏 XX 号电梯群控连接',''),('05A0','群控通讯协议不相容','群内所有电梯 MZ1 卡使用相同版本',''),('05A8','群控通讯协议与群控处理器不兼容','检查 MZ1 卡传输版本和群控处理器',''),('05C ','的地叫车未服务','叫车已分配但指定电梯未服务',''),('05C0','特殊程序复归运作','暂停时间到而复归',''),('05XX','TCM 群控特殊程序错误信息。出现在下列的错误指示之后','询问 TU 或 VTS 在这些错误发生时。XX＝详细错误叙述数据',''),('05YY','群控命令错误（有缺陷的 MG 卡或群控接线失败）','TCI：检查 MG 卡或群控接线TCM：检查群控扁平电缆（MZ1 卡）软件错误：确认工作程序版本','2'),('05b0','DCS 重置：05XX 伴随发生ZES＝目标输入终端机','ZES 维持执行。检查电压供应及 CAN 与各ZSE 的连接XX＝相对应停楼',''),('05b1','来自 DCS 不明的回应：Hallo(=起始程序)05XX伴随发生','XX＝相对应停楼',''),('05b2','DCS 发出不明的准备好的讯息（＝起始终结）05XX伴随发生','XX＝相对应停楼',''),('05b3','DCS 起始值暂停，程序数据开端，05XX 伴随发生','起始 DSC 失败，检查电压及连接个别 ZSE 的讯号传输线XX＝相对应停楼',''),('05b4','DCS 默认值暂停，程序数据末端，05XX 伴随发生','',''),('05b5','DSC-电梯动作暂停，05XX 伴随发生','无来自 DSC 周期性响应，检查电压及连接个别 ZSE 的讯号传输线XX＝相对应停楼',''),('06XX','停楼 XX 闭锁失败 3 次导致紧急停止','检查停楼XX闭锁开关或机械部分','M2'),('0701','主门 TSO 错误：TO 命令输出 30 秒而 TSO无讯号。CPU 在到时间后将仿真 TSO 讯号，使门能恢复正常动作','TSO 缺陷或调整不良。有闭锁装置的电梯门，不闭锁异常可能因门控制系统无法执行 TO 命令',''),('0702','主门 TSO 错误（参考 0b04）','TK 导通而 TSO 显示主门开启。重置引起 N1',''),('0801','副门 TSOD 错误','参考 0701','1'),('0802','副门 TSOD 错误','参考 0702','N3'),('09NN','叫车或命令已存在，但电梯仍停留在某一楼层超过 4min 没有动作','可能门再开装置造成，参考 0500 功能 0d 栏。有反旋装置之油压梯，可能因车厢过低或限速器张力轮不顺而引起（参考后面范例）','M3'),('0A2F','钢索松弛','',''),('0A30','磨到外门区域','',''),('0A31','车厢门未关','',''),('0A32','停楼外门未闭锁','',''),('0A33','油温超过 70℃','',''),('0A34','油平面监视','',''),('0A46','保养开关 ON','',''),('0A47','保养开关 OFF','',''),('0AAA/0AXX','特殊程序错误Tech-in 错误（主边升降道 Tech-in；0bXX 副边升降道）参考工作 Tech-in 通告（MA 13 6510.046）','可能比对命令程序操作错误。AA＝表列叙述错误（操作错误说明）如果错误发生于 Tech-in AF0D 或 AF0C，0AXX 表示停楼 XX 的 MS2 未被分派','2'),('0C01','CPU：MZ1 到操作系统失败','CPU 到 MZ 传输的问题','S1'),('0C02','CPU：MZ1 到操作系统失败','CPU 到 MZ 传输的问题','S1'),('0C03','CPU：MZ1 到操作系统失败','','S1'),('0C04','CPU：车厢的开始值≠参考值','a)电梯特殊程序不符b)传输扁平电缆接触不良检查电梯特殊程序 EPROM（地址）',''),('0C05','CPU：MP 的开始值 1≠参考值 1','a)MP 卡不正常b)MP 卡指拨开关编码不正确c)扁平电缆联络异常检查电梯特殊程序 EPROM（地址）',''),('0C06','CPU：MP 的开始值 2≠参考值 2','a)MP 卡不正常b)MP 卡指拨开关编码不正确c)扁平电缆联络异常检查电梯特殊程序 EPROM（地址）',''),('0C07','CPU：机房扁平电缆开始值 1≠参考值 1','参考上列 a)及 c)',''),('0C08','CPU：机房扁平电缆开始值 2≠参考值 2','参考上列 a)及 c)',''),('0C09','CPU：MF4 的开始值 1≠参考值 1','MF4 卡正常，但没有来自 MF4 的确认接收讯号',''),('0C0A','CPU：MF4 的开始值 2≠参考值 2','MF4 卡正常，但没有来自 MF4 的确认接收讯号',''),('0C0C','CPU：MF4 的开始值 4≠参考值 4','MF4 卡正常，但没有来自 MF4 的确认接收讯号',''),('0C0E','CPU：FKZ 的开始值 2≠参考值 2','FKZ＝车厢附件（如门系统、启动补偿装置）',''),('0C0b','CPU：MF4 的开始值 3≠参考值 3','MF4 卡正常，但没有来自 MF4 的确认接收讯号',''),('0C0d','CPU：FKZ 的开始值 1≠参考值 1','FKZ＝车厢附件（如门系统、启动补偿装置）',''),('0C10','CPU：MZ1 的默认值计时错误','没有来自 MZ1 的确认接收讯号','S1'),('0C11','CPU：MZ1 的默认值计时错误','起始及完成接收皆未被确认','S1'),('0C12','CPU：MZ1 的默认值计时错误','起始及完成接收确认超过 20 秒','S1'),('0C13','CPU：MZ1 确认标准重置','MZ1 错误，使用 V10 以后程序','N1'),('0C1C','CPU：无 CPI 联络讯号','F31C 伴随发生',''),('0C20','MZ1：坑道缓冲区过载','坑道/车厢数据无法读取。可能 MZ1、坑道、车厢传输线接头不良',''),('0C21','MZ1：坑道缓冲区过载','坑道/车厢数据无法读取。可能 MZ1、坑道、车厢传输线接头不良',''),('0C22','MZ1：坑道缓冲区过载','坑道/车厢数据无法读取。可能 MZ1、坑道、车厢传输线接头不良',''),('0C23','MZ1：坑道缓冲区过载','坑道/车厢数据无法读取。可能 MZ1、坑道、车厢传输线接头不良',''),('0C24','MZ1：坑道缓冲区过载','坑道/车厢数据无法读取。可能 MZ1、坑道、车厢传输线接头不良',''),('0C25','MZ1：坑道缓冲区过载','坑道/车厢数据无法读取。可能 MZ1、坑道、车厢传输线接头不良',''),('0C30','MZ1：坑道扁平电缆有缺失','重新起始超过 MZ1 限制','N1'),('0C31','MZ1：坑道扁平电缆传输错误','MZ1 对坑道检测错误',''),('0C32','MZ1：坑道扁平电缆资料过载','',''),('0C3A','MZ1：MF3D 传输程序流失','',''),('0C3C','MZ1：MF3 回应缺失','MZ1 到车厢传输线端子不良',''),('0C3b','MZ1：MF3 传输程序流失','',''),('0C3d','MZ1：MF3 回应缺失','MZ1 到车厢传输线端子不良',''),('0C40','MZ1：车厢缓冲区过载','已读取超出 MF1 能处理的数据量',''),('0C42','MZ1：车厢缓冲区过载','已读取超出 MF1 能处理的数据量',''),('0C43','MZ1：车厢缓冲区过载','已读取超出 MF1 能处理的数据量',''),('0C45','MZ1：车厢缓冲区过载','已读取超出 MF1 能处理的数据量',''),('0C50','MZ1：车厢扁平电缆缺陷','重新起始超过 MZ1 限制',''),('0C51','MZ1：车厢扁平电缆传输错误','重新起始超过 MZ1 限制',''),('0C52','MZ1：车厢扁平电缆资料过载','重新起始超过 MZ1 限制',''),('0C53','MZ1：车厢扁平电缆要求重置','重新起始超过 MZ1 限制',''),('0C60','MZ1：频率分配异常','CAN 测试',''),('0C70','CANL 测试：频率分配异常','CAN 控制器被初始化',''),('0C73','CANL 测试：CAN 控制器要求重置','CAN 控制器被初始化',''),('0C74','CANL 测试：登录状态错误（EMC）','CAN 控制器被初始化',''),('0C75','CANL 测试：输出缓冲区过载','',''),('0C76','CANL 测试：输出缓冲区过载','',''),('0C78','CANS 测试：频率分配异常','CAN 控制器被初始化',''),('0C7A','CANS 测试：坑道资料过载','',''),('0C7C','CANS 测试：登录状态错误（EMC）','',''),('0C7b','CANS 测试：坑道扁平电缆重置请求','CAN 控制器被初始化',''),('0C80','MF3：MF3 重置','',''),('0C81','MF3：MZ1 传输程序失效','',''),('0C85','MF3：坑道资料过载','超过 MF3 能处理数据',''),('0C86','MF3：坑道扁平电缆传输错误','MF3－CAN 传输缺失记录',''),('0C87','MF3：坑道扁平电缆缺失','',''),('0C88','MF3：确认使用 MF2 不允许','＞56HS 使用 MF2；检查',''),('0C89','MF3：CAN 芯片异常','要求或频率重置',''),('0C8A','MF3：MF3 起始错误','',''),('0CA0','MF3D：MF3 重置','',''),('0CA1','MF3D：MZ1 传输程序失效','',''),('0CA5','MF3D：坑道资料过载','超过 MF3D 能处理数据',''),('0CA6','MF3D：坑道扁平电缆传输错误','MF3D- CAN 传输缺失记录',''),('0CA7','MF3D：坑道扁平电缆缺失','',''),('0CA8','MF3D：确认使用 MF2 不允许','＞56HS 使用 MF2；检查',''),('0CA9','MF3D：CAN 芯片异常','要求或频率重置',''),('0CAA','MF3D：MF3 起始错误','',''),('0CE0','重置','',''),('0CE2','内存数据过载','',''),('0CE3','扁平电缆错误','',''),('0CE4','扁平电缆干扰','',''),('0CE5','不完整的传输数据','',''),('0CE8','运转时间错误','',''),('0CE9','监视器','',''),('0CEA','过电流','',''),('0CEC','过热-散热片','',''),('0CEE','限速器无作用','',''),('0CEF','F2/1：热耦室','',''),('0CEb','过电压','',''),('0CEd','过热-门马达','',''),('0CFF','CPU：来自 MZ1 不明确命令','如此错误发生，参考内存位置 dE2F 及 dE3F并连同错误的卡片寄给 VTS 或 QMS 部门注意：重置将会清除指定的内存位置',''),('0Cd0','重置','',''),('0Cd2','内存数据过载','',''),('0Cd3','扁平电缆错误','',''),('0Cd4','扁平电缆干扰','',''),('0Cd5','不完整的传输数据','',''),('0Cd8','运转时间错误','',''),('0Cd9','监视器','',''),('0CdA','过电流','',''),('0CdC','过热-散热片','',''),('0CdE','控制器无作用','',''),('0CdF','F2/1：热耦室','',''),('0Cdb','过电压','',''),('0Cdd','过热-门马达','',''),('0E00','从 MW1 到 CPU 传输缺失','','1'),('0F0A','设置旗标开关 ON','开关位于 MZ 或 MZ1 上',''),('0F0C','电话程序设置旗标','服务状态开关 ON',''),('0F0E','设置旗标开关 OFF','开关位于 MZ 或 MZ1 上',''),('0F0F','电梯功能开启','保养平台关闭','Reset'),('0F0b','无机房电梯','保养平台开启 Reset',''),('0F0d','电话程序设置旗标','服务状态开关 OFF',''),('0FZZ','设置旗标','ZZ＝旗标编号',''),('0b01','主门光栅错误','光栅遮断超过 EPROM 特别程序规定时间；预防 0900 产生（错误可能发生在分离控制＆光栅＆TCI 版本 06.95 以上）','M2'),('0b02','副门光栅错误','参考 0b01','M2'),('0b03','群控失败超过1小时','电梯脱离群控。例如专用、被占用等（软件错误；使用 TCI 自 06.95 的工作版本）','M2'),('0b04','TSO 错误－主门','虽然门关闭，但 TSO 表示门开启','SM2'),('0b05','TSOD 错误－副门','虽然门关闭，但 TSO 表示门开启','SM2'),('0b06','地震感知器动作','仅使用 MCX CPU','SM1'),('0b07','车厢保养驾驶输入到 MF3 讯号不良','仅使用 MCX CPU（自工作版本 V51＆V81）',''),('0d1b','监视 MW1 参考-实际值（B＝运转状态）','缺少脉冲讯号（仅在保养运转状态）；CPU 检出缺乏脉冲','N'),('0d2b','脉冲顺序监视：上行时 A 频在 B 频之前','脉冲频 A＆B 被拌和。正确的脉冲顺序显示于 ESA 卡（Iso60）或 NIM 卡（Iso25M）','N'),('0d3b','实际值＞参考值（+10﹪在 VN；+100﹪在VI；+80﹪在 VJ；+50﹪在 VNS）','如果紧急停止的参考值已经到 0 而实际值仍在运行','N'),('0d4b','实际值＜参考值（-10﹪在 VN；-100﹪在 VI；-80﹪在 VJ；-50﹪在 VNS）','错误可能发生在：门闭锁开关不良（没有14XX），缺乏脉冲讯号，MW1 参考值电压＞9.8V，加速斜率设定太陡峭（实际值无法达成），驱动控制器太迟钝；I 成分设定过高等因素','N'),('0d5b','实际值＞参考值','实际值＞额定+10﹪','N'),('0d6b','驱动侧控制器停止（仅在模拟控制器如Iso25M）','设定驱动包含控制范围（非数字控制）加速设定太陡峭，马达开关设定不适当，齿轮油太冷','N'),('0d7b','回授参考值（MW1）计算未水平','虽车厢位于水平位置，但 MW1 计算值未达水平＞3 ㎜此错误讯息可能产生。（12.95 以上软件错误码）','N'),('0d8b','回授参考值（MW1）停滞速度＞0.25m/s','MW1 表示停滞速度＞0.25m/s。原因：在停滞速度脉冲发电机仍产生脉冲；脉冲信号线（隔离线）有干扰信号','N'),('10YY','CPU 卡缺失','Reset 将伴随发生','N'),('1101','TCM：群控的 CAN 扁平电缆缺失','MZ1 上群控 CAN 扁平电缆失误。使用包含群控 CAN 扁平电缆的 MZ1',''),('11YY','MG 卡缺失','群控输入/输出芯片失效','1'),('12XX','计算位置不等于车厢实际位置','非 LK 错误。楼层计算程序在停车状态的错误','3'),('13XX','被裁定的位置不等于车厢实际位置','参考 12XX','3'),('14XX','停楼 XX 闭锁开关 RK 打开','RK 开关在运转期间被打开。原因：外门用钥匙开启；TSM 或闭锁磁铁动作不完整；凸轮马达调整不当；凸轮或闭锁凸轮在 by-passing时摩擦','N8'),('15XX','计算位置不等于实际位置','楼层计算程序在停滞起动前状态的错误','2'),('16YY','MW/MW1：位置差异','仅发生在有 MW/MW1 的电梯','3'),('17YY','CPU－MW/MW1 错误','仅发生在有 MW/MW1 的电梯（储存过满）','N1'),('18XX','停楼 XX 副门闭锁开关 RKD 打开','参考 14XX','N8'),('19NN','门区域未被认可（CPU 无法辨识楼码片，但已开始着床）','在停车状态 LK 到门区域信号失效。对应到功能 0500，05 列说明（参考后面范例）','N2'),('1AYY','LK 检测器检出错误：应暗实际亮','可能发生错误：LK 或楼码片的问题；钢索打滑或控制器不稳定；回授有缺陷。','N8'),('1CNN','不明确的运转','已起动运转但无有效命令','4'),('1ENN','在 bypassing 记号最终停楼楼码片或保养驾驶限制开关 IFO/IFU 无延迟','车厢位置 Bit20 在 25 之上；Bit26（1）被激磁；Bit27（1）被激磁。NN 是 16 进位表示（参考后面范例）','3'),('1F00','机房扁平电缆中断','',''),('1F01','机房扁平电缆错误','',''),('1F02','机房扁平电缆过载','',''),('1F03','输入缓冲区过载','',''),('1F04','电路板过载（reset）','',''),('1F05','无交握传输程序 交握是定义如两块数据电路板周期性数据交换','',''),('1F80','机房扁平电缆被中断','',''),('1F81','机房扁平电缆错误','',''),('1F82','机房扁平电缆过载','',''),('1F83','输入缓冲区过载','',''),('1F84','FIS：重置','紧急停止或电源重置将被触发（MC1）','N1'),('1F85','FIS：外在的接触器交握程序 2X 失误','',''),('1F86','FIS：外在的周期性传输程序接触器失败','','N1'),('1F87','FIS：内部的错误','',''),('1F88','MM/ME：机房扁平电缆被中断','',''),('1F89','MM/ME：机房扁平电缆错误','',''),('1F8A','MM/ME：机房扁平电缆过载','',''),('1F8C','MM/ME：重置','',''),('1F8E','MM/ME：MM 或 ME 被 MCx 起始','',''),('1F8F','MM/ME：因 MM 或 ME 而重置','',''),('1F8b','MM/ME：输入缓冲区过载','',''),('1F8d','MM/ME：无传输程序交握','',''),('1F90','MQ1：机房扁平电缆被中断','',''),('1F91','MQ1：机房扁平电缆错误','',''),('1F92','MQ1：机房扁平电缆过载','',''),('1F93','MQ1：输入缓冲区过载','',''),('1F94','MQ1：重置','',''),('1FA0','MH3：机房扁平电缆被中断','',''),('1FA1','MH3：机房扁平电缆错误','',''),('1FA2','MH3：机房扁平电缆过载','',''),('1FA3','MH3：输入缓冲区过载','',''),('1FA4','MH3：重置','',''),('1FA5','MH3：来自 MH3，两个交握错误','',''),('1FA6','MH3：控制器到 MC1/MC3 的周期性传输程序失败','',''),('1FA7','MH3：MH3 卡内部错误','',''),('1FA8','MH3：安全状况后重置','',''),('1bYY','LK 检测器检出错误：应亮实际暗','可能发生错误：LK 或楼码片的问题；钢索打滑或控制器不稳定；回授有缺陷。','N5'),('1dYY','紧急停止（错误的运转命令）','无或两方向运转命令产生','N3'),('20TT','SR 模块错误','SR 作用时，侦测 SR 回到 CPU 讯号时间。TT＝16 进位数字乘以 50ms。同错误码 2300',''),('2100','EEPROM 错误（28C64 芯片）','EEPROM 内存储器位置缺陷','S1'),('2200','SR 模块错误（分辨率＞100ms）','经由 CPU 通道 I 中断 100ms 后，侦测 SR 回到 CPU 讯号仍存在','N4'),('2300','SR 模块错误','与错误码 4300 同，但不会停止（德国不允许）','8'),('2400','CPU：EEPROM 缺陷','EEPROM 内存储器位置缺陷。重插 EEPROM 或 CPU SM3按钮检查',''),('2502','外叫车缺陷','主门侧外叫车下行不良',''),('2504','外叫车缺陷','主门侧外叫车上行不良',''),('2520','外叫车缺陷','副门侧外叫车下行不良',''),('2540','外叫车缺陷','副门侧外叫车上行不良',''),('2604','保养平台开启同时极限开关闭路','极限开关被短路或保养平台输入讯号不良。无运转命令的可能；除了车厢保养外电梯将停止运转。错误信息于 3 秒后产生','MS'),('2605','保养平台关闭，极限开关既不开也不关','极限开关和配重冲突或极限开关正被 closed;仅紧急运转下行可允许。错误信息于 3 秒后产生','MS'),('2606','保养平台开启，极限开关既不开也不关','过渡状态，极限开关 open 或不良；无运转命令的可能。除了车厢保养外电梯将停止运转。','MS'),('2607','保养平台开启，极限开关既开又关','开关不良，无运转命令的可能。电梯将停止运转。错误信息于 3 秒后产生','MS'),('2608','保养平台开启，极限开关既开又关','开关不良，无运转命令的可能。电梯将停止运转。错误信息于 3 秒后产生','MS'),('2609','无机房电梯','尽管电梯正常运作，SR 模块复检功能动作','MS'),('260A','无机房电梯','如果最上停楼未到达（极限开关动作）SR 模块复检功能缺失',''),('27XX','仅发生在使用MC1 或MC2 的TCM 电梯（XX＝意义参考补充说明版本 MA12 6510.062）','监视输入或 RFS 模块（relay flat pit）不良','MS'),('2800','低负载运转期间失败','','N'),('284X','低负载运转时间超过 30 秒','','N'),('288X','低负载运转上行时间超过 30 秒','','N'),('2900','虽然安全回路打开，但车厢盖板合拢','','MS'),('2910','连续 3 次低负荷运转失败','','MS'),('29XX','车厢盖板不良','','MS'),('2A00','TMI 接触器确认','新－旧：00 00',''),('2A11','TMI 接触器确认','新－旧：01 01',''),('2A12','TMI 接触器确认','新－旧：01 10',''),('2A20','TMI 接触器确认','新－旧：10 00',''),('2A21','TMI 接触器确认','新－旧：10 01',''),('2A22','TMI 接触器确认','新－旧：10 10',''),('2A32','TMI 接触器确认','新－旧：11 10',''),('2A33','TMI 接触器确认','新－旧：11 11',''),('2C00','变动检查错误（LK/LN 于重拉水平）','LK＆LN 检测将重拉水平状态。不允许向上时 LK 亮 LN 暗；向下时 LK 暗 LN 亮。原因：过度的重拉水平速度；LK/LN 间距太小（如果调整需重新 Tech-in）','5'),('2E00','重拉水平时间＞7S（自工作版本 02.96/26 增加到≦20S）','重拉水平速度太慢；油压梯基本容积设定错误，致使车厢开始移动时间过长','N2'),('2F00','重拉水平距离＞4 倍重新起动单位','使用标准楼码片 4 倍重新起动单位＝8 ㎝','N1'),('2b00','在停滞操作状态开始闭锁超过 60 秒','',''),('2d00','SR 模块异常','重拉水平期间到 CPU 检查讯号异常。检查区域开关 ZS、检查 KTK','N2'),('3000','LK 读取错误（调整运转期间紧急停止）','调整运转期间楼码无法辨识。需坑道资料Tech-in','N2'),('3100','LK 错误','检查 LK',''),('3200','LK 错误','检查 LK',''),('3300','LK 错误','检查 LK',''),('3400','LK 错误','检查 LK',''),('3500','激磁选择器错误','楼码片出发勾无法辨识（检查 LK）','2'),('3600','激磁选择器错误','水平窗口感测是暗的（检查 LK 和楼码-含磁簧近接开关选择器）','2'),('3700','激磁选择器错误','在停止操作状态 ZSE 未激磁','2'),('3C00','LK 错误（读取错误）','楼码与 Tech-in 时读入楼码不符，仅着床时会紧急停止。原因：LK 传感器跳动；牵引力太低（主钢索打滑）；回授发电机打滑（油压梯）；LK 脉冲线不良；楼码片脏','N4'),('3E00','防旋装置异常（限速器起动）','MAS 电磁动作但限速器上开关开启失败。原因：限速器上开关故障；限速器上闭锁爪卡住（如果合闸杆停止在棘轮上，电磁冲程相对小）。校正：放置两只垫圈（6 ㎜）于电磁和固定架间','SM3'),('3F00','防旋装置异常（限速器抑制）','电磁被释放但开关打开失败。原因：开关故障；计时模块 ZSP 接触器设定太久，限速器模块失败','SM3'),('3b00','楼码水平窗口错误','',''),('3d00','LK 错误（楼码片）','抵达码不等于出发码（仅发生于 by-passing）',''),('4000','警铃动作','特殊工作程序动作',''),('4100','运转监视装置缺失（缺少脉冲讯号）','CPU 的运转监视装置中断（牵引式电梯缺少脉冲＞4S 或油压电梯＞8S）。原因：脉冲发电机故障；油压梯基本容积设定错误','SM1'),('4200','运转时间监视','在着床及调整运转速度时间太久：LK 无明暗变化 VN＞20s VJ＞45s','SM3'),('4300','SR 模块异常（闭锁开关未桥接）','CPU 检查缺失。原因:SR 模块异常，ZS 开关不良，ZSE 及 LK 进入楼码片透入深度不正确','SM8'),('4400','SR 模块异常（仅油压梯最低楼层停止）','如发生于较高楼层同 4300；如仅发生于最低楼层原因：错误发生于油压梯，一个回归最低楼层错误必伴随发生','SM2'),('4500','紧急停止按钮被执行','仅挪威版中（参考数据图表）','N'),('4600','维修保养开关 ON','仅顾客特殊功能有效',''),('4700','维修保养开关 OFF','仅顾客特殊功能有效',''),('4800','重新准备好讯息','电梯重新准备好自发的讯息','N'),('4900','调整运转状态超过内定值（5min）','检查调整运转时间为何无法于 5min 内完成','M2'),('4A00','CPU 与 MW/MW1 间传输错误','MW/MW1 卡在较高质量装置缺失','N2'),('4C00','MW/MW1：在测试模式','MW/MW1 卡上 S9 接通',''),('4E00','路径计算器 MW/MW1：','到路径计算器传输（RST5.5）缺失',''),('4F00','到 CPU 的接触器检查回报（设定值与实际值比较电路接触器）','在调整运转或尝试数次调整运转时接触器检出错误','SM2'),('4b00','MW/MW1：计算位置不等于实际位置','MW/MW1 辨识确认勾缺失。原因：正常运转伴随紧急停止运转（非调整运转）','N2'),('4d00','MW/MW1：未准备完成','MW/MW1 自 CPU 重置','N2'),('5000','停止带有还原及 TCM 控制的集体错误','原因：TCM 错误 C01，C02，C03，C04，C11，C12 发生（初始值的问题）','SM2'),('5100','运转监视','缺少脉冲讯号＞4S','N2'),('5200','紧急停止后调整运转','紧急停止后无重置的调整运转',''),('5300','随调整运转之后的运行','随调整运转之后的运行（紧急停止）',''),('5400','CPU 缺失（监视中断）','CPU 计算器缺失',''),('5500','重置','重置导因于程序重新起动（主电源 OFF/ON或电源供应中断）原因：％V 电压设定不正确；电源供应不稳定等',''),('5501','MC2 群控重置','DC24V 被断线',''),('5600','CPU 缺失（TRAP）','',''),('5600','分配错误致使中断执行','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('5601','记录轨迹中断','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('5602','非可遮蔽的中断','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('5603','断点中断','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('5604','INT（断路器）0 检测过剩致使中断执行','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('5605','系统限制，中断执行','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('5606','未使用的输出码（opcode）致使中断执行（X)错误 8900 将伴随发生','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('5607','漏失输出码（opcode）致使中断执行','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('5608','定时器 0 中断','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('5609','AMD 备份中断','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('560A','DMA（直间储存器地址）0 或 INT 5','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('560C','INT 0','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('560E','INT 2','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('560F','INT 3','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('560b','DMA 1 或 INT 6','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('560d','INT 1','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('5610','INT 4','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('5611','不同步串行埠 0 中断','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('5612','定时器 1 中断','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('5613','定时器 2 中断','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('5614','不同步串行埠 1 中断','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('56FF','不明确的软件中断（5620 到 56FF）','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('56…','不明确的中断','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS','N'),('5700','调整运转','紧急停止及上述的错误后致使进入调整运转',''),('5800','紧急停止','某些错误后紧急停止',''),('5900','正停止于紧急停止事件中','如果特殊程序中的错误导致紧急停止发生时，电梯将被停止。地址码：A570 到 A57F（16 个错误能被写入；对照第 3 部分内存位置）','SM1'),('5A00','CPU-MW/MW1 错误','MW/MW1：信号准备好的缺失','SM2'),('5C00','CPU-MW/MW1 错误','MW/MW1：传输后无读取埠中断','SM2'),('5E00','CPU-MW/MW1 错误','MW/MW1：二次不明传输（无重复）','SM2'),('5F00','EK 错误（EK＝极限开关接触器）','EK 错误后将停止于最低停楼','MB'),('5b00','CPU-MW/MW1 错误','MW/MW1：TCI 重置后请求传输程序缺失','SM2'),('5d00','CPU-MW/MW1 错误','MW/MW1：一次不明传输（重复）',''),('6000','安全回路','EK 开路运转期间 EK 中断（不含调整运转）。在一些装置如 Isostop60（API）中，因驱动监视接触器于 EK 前，故释放时也会发生','MN'),('6100','安全回路','HK 开路 紧急停止或安全钳开关开路','N'),('6200','安全回路','TK 开路 内门开关 KTK 或 KTKD 于运转期间中断','N'),('6300','安全回路','KT 开路 闭锁开关 RK 或 RKD 于运转期间中断','N'),('6400','主机马达热藕开关中断','检查 PTC 热藕开关或 PTC 热藕接触器端子','MN'),('6500','00-00 0','接触器放开1 接触器吸上',''),('6600','00-01','0 接触器放开1 接触器吸上',''),('6700','00-10','0 接触器放开1 接触器吸上',''),('6800','00-11','0 接触器放开1 接触器吸上',''),('6900','01-00','0 接触器放开1 接触器吸上',''),('6A00','01-01','0 接触器放开1 接触器吸上',''),('6C00','01-11','0 接触器放开1 接触器吸上',''),('6E00','10-01','0 接触器放开1 接触器吸上',''),('6F00','10-10','0 接触器放开1 接触器吸上',''),('6b00','01-10','0 接触器放开1 接触器吸上',''),('6d00','10-00','0 接触器放开1 接触器吸上',''),('7000','10-11','0 接触器放开1 接触器吸上',''),('7100','11-00','0 接触器放开1 接触器吸上',''),('7200','11-01','0 接触器放开1 接触器吸上',''),('7300','11-10','0 接触器放开1 接触器吸上',''),('7400','11-11','0 接触器放开1 接触器吸上',''),('7500','触发信号传感器 KT 缺失','适用于 7500 到 7800：检查个别传感器和MQ/MQ1，如有需要重新插入。用诊断器 0500 功能检查','2'),('7600','触发信号传感器 TK 缺失','检查个别传感器和MQ/MQ1，如有需要重新插入。用诊断器 0500 功能检查',''),('7700','触发信号传感器 HK 缺失','检查个别传感器和MQ/MQ1，如有需要重新插入。用诊断器 0500 功能检查',''),('7800','触发信号传感器 EK 缺失','检查个别传感器和MQ/MQ1，如有需要重新插入。用诊断器 0500 功能检查',''),('7900','温度感测缺失','检查温度传感器，如必要 MZ 卡重插',''),('7A00','控制器监视缺失','检查监视传感器，如必要 MZ 卡重插',''),('7C00','虽然运转命令存在但 CPI 控制器断线','仅发生于含外部参数设定的 CPI（检查控制器内部的监视功能）','N5'),('7E01','MH3：写入 EEPROM 期间错误','',''),('7E02','MH3：联机设定期间 modem 无法辨识','',''),('7E03','MH3：重新搜寻 modem','',''),('7E04','MH3：从动的到主动的联机切断','',''),('7E05','MH3：写入 EEPROM 期间错误','',''),('7E06','MH3：写入 EEPROM 期间错误','',''),('7E07','MH3：写入 EEPROM 期间错误','',''),('7E08','MH3：DOS 下载请求','',''),('7E09','MH3：最初状态重置','',''),('7E0A','MH3：写入 EEPROM 期间错误','',''),('7EA4','MC3：从 MH3 重置','','N1'),('7EA5','MC3：来自 MH3 两个交握程序错误','',''),('7EA6','MC3：到 MH3 周期性传输缺失','','N1'),('7EA7','MC3：储存状态后重置','自 MH3 完成需求','N1'),('7Exx','MH3：xx＝00…7F，来自 MH3 内部的错误MC3：xx＝80…FF，MC3 辨识 MH3 错误','',''),('7F8E','MCx 触发 MM 或 ME 的起始','',''),('7F8F','起因于 MM 或 ME 的重置','','N1'),('7F8d','来自 MM 或 ME 的交握传输','',''),('7Fxx','MM/ME：XX＝00…7F 是 MM 或 ME 内部的错误','MCx：XX＝80…FF 是 MCx（＝MC1，MC2 或 MC3）辨识 MM 或 ME 的错误','Xxx'),('7b00','DC24V 电压供应缺失','检查电压（MQ 卡电压亦检查）','MBS'),('7d00','CPI：无错误','',''),('7d01','CPI：控制电压 ON','',''),('7d02','CPI：监视器错误','',''),('7d03','CPI：SMR（状态监视程序）缺失','',''),('7d04','CPI：SMR 到 TCM 控制','',''),('7d05','CPI：EEPROM 错误','',''),('7d06','CPI：散热器过热','',''),('7d07','CPI：驱动马达过热','',''),('7d08','CPI：接地缺陷讯息','',''),('7d09','CPI：主电源未确认','',''),('7d0A','CPI：直流环节电压过低','查询整个参数-输入面板',''),('7d0C','CPI：直流环节电压过高','',''),('7d0E','CPI：过电流','',''),('7d0F','CPI：主电压过高','',''),('7d0b','CPI：有效电力的允许脉动','',''),('7d0d','CPI：错误堆栈删除','',''),('7d10','CPI：DSP 时间错误','DSP＝CPI 内数字信号处理器',''),('7d11','CPI：±15V 或 24V 过低','',''),('7d12','CPI：No.18 错误（一般未使用）','',''),('7d13','CPI：CAN 扁平电缆错误','',''),('7d14','CPI：电压实际值≠参考值±10﹪','',''),('7d15','CPI：DSP 电流控制器错误','',''),('7d16','CPI：DSP 重置','',''),('7d17','CPI：到 DSP 的不明讯号','',''),('7d18','CPI：传输参考值编号错误','',''),('7d19','CPI：运转接触器有问题','',''),('7d1A','CPI：档板设定','',''),('7d1C','CPI：脉冲发电机缺失','',''),('7d1E','CPI：煞车错误','',''),('7d1F','CPI：马达或煞车过热','',''),('7d1b','CPI：脉冲发电机刻度范围错误','',''),('7d1d','CPI：成功的脉冲发电机刻度','',''),('7d20','CPI：sin-cos 发电机错误','',''),('7d21','CPI：回授放大组件未准备好','',''),('7d84','MC3：CPI 控制器重置','','N1'),('7d85','MC3：来自 CPI 的两个交握讯号流失','交握是定义如两电路板间周期性数据转换',''),('7d86','MC3：到 CPI 周期性传输的缺失','','N1'),('7dxx','CPI：事件 xx','',''),('8000','错误的车厢命令','当电梯位于最低楼仍命令下行','N1'),('8100','错误的车厢命令','当电梯位于最高楼仍命令上行','N1'),('8200','不明的车厢位置','注：重新 Tech-in，如失败检查 CPU 的 5V电压或更换 CPU 上的 EEPROM','N3'),('8300','不明的车厢位置','注：重新 Tech-in，如失败检查 CPU 的 5V电压或更换 CPU 上的 EEPROM',''),('8400','不明的车厢位置','注：重新 Tech-in，如失败检查 CPU 的 5V电压或更换 CPU 上的 EEPROM',''),('8500','不明的车厢位置','注：重新 Tech-in，如失败检查 CPU 的 5V电压或更换 CPU 上的 EEPROM',''),('8600','煞车检出电路失误（自 TCI 工作程序版本 06.95/25 以后）','检查煞车检出传感器的设置。监视器可经由tech-in 的 AF0d 功能取消。','MNS'),('8601','整个安全回路接通期间，煞车被中断开','有缺陷',''),('8701','额定速度 VN','说明：8701-870c减速斜率等内存位置未被写入程序或写入不恰当。在这个部分，电梯特殊程序必须被制成现成的，在改编程序形式中命令程序部门，指定错误码编码。特殊程序内存位置可使用诊断器单元 I 查询也可参考功能 0000 内存位置',''),('8702','最大速度 VCON','说明：8701-870c减速斜率等内存位置未被写入程序或写入不恰当。在这个部分，电梯特殊程序必须被制成现成的，在改编程序形式中命令程序部门，指定错误码编码。特殊程序内存位置可使用诊断器单元 I 查询也可参考功能 0000 内存位置',''),('8703','加速斜率 ａ','说明：8701-870c减速斜率等内存位置未被写入程序或写入不恰当。在这个部分，电梯特殊程序必须被制成现成的，在改编程序形式中命令程序部门，指定错误码编码。特殊程序内存位置可使用诊断器单元 I 查询也可参考功能 0000 内存位置',''),('8704','减速斜率 －ａ','说明：8701-870c减速斜率等内存位置未被写入程序或写入不恰当。在这个部分，电梯特殊程序必须被制成现成的，在改编程序形式中命令程序部门，指定错误码编码。特殊程序内存位置可使用诊断器单元 I 查询也可参考功能 0000 内存位置',''),('8705','急拉','说明：8701-870c减速斜率等内存位置未被写入程序或写入不恰当。在这个部分，电梯特殊程序必须被制成现成的，在改编程序形式中命令程序部门，指定错误码编码。特殊程序内存位置可使用诊断器单元 I 查询也可参考功能 0000 内存位置',''),('8706','急拉 1','说明：8701-870c减速斜率等内存位置未被写入程序或写入不恰当。在这个部分，电梯特殊程序必须被制成现成的，在改编程序形式中命令程序部门，指定错误码编码。特殊程序内存位置可使用诊断器单元 I 查询也可参考功能 0000 内存位置',''),('8707','急拉 2','说明：8701-870c减速斜率等内存位置未被写入程序或写入不恰当。在这个部分，电梯特殊程序必须被制成现成的，在改编程序形式中命令程序部门，指定错误码编码。特殊程序内存位置可使用诊断器单元 I 查询也可参考功能 0000 内存位置',''),('8708','急拉 3','说明：8701-870c减速斜率等内存位置未被写入程序或写入不恰当。在这个部分，电梯特殊程序必须被制成现成的，在改编程序形式中命令程序部门，指定错误码编码。特殊程序内存位置可使用诊断器单元 I 查询也可参考功能 0000 内存位置',''),('8709','急拉 4','说明：8701-870c减速斜率等内存位置未被写入程序或写入不恰当。在这个部分，电梯特殊程序必须被制成现成的，在改编程序形式中命令程序部门，指定错误码编码。特殊程序内存位置可使用诊断器单元 I 查询也可参考功能 0000 内存位置',''),('870A','调整运转速度 VJ','说明：8701-870c减速斜率等内存位置未被写入程序或写入不恰当。在这个部分，电梯特殊程序必须被制成现成的，在改编程序形式中命令程序部门，指定错误码编码。特殊程序内存位置可使用诊断器单元 I 查询也可参考功能 0000 内存位置',''),('870C','保养速度 VJ','说明：8701-870c减速斜率等内存位置未被写入程序或写入不恰当。在这个部分，电梯特殊程序必须被制成现成的，在改编程序形式中命令程序部门，指定错误码编码。特殊程序内存位置可使用诊断器单元 I 查询也可参考功能 0000 内存位置',''),('870b','重新调整运转速度 VN','说明：8701-870c减速斜率等内存位置未被写入程序或写入不恰当。在这个部分，电梯特殊程序必须被制成现成的，在改编程序形式中命令程序部门，指定错误码编码。特殊程序内存位置可使用诊断器单元 I 查询也可参考功能 0000 内存位置',''),('87PP','特殊程序中必要的 MW1 参数值缺乏。个别的错误参数能被限定于基本变量 PP 上（如 8704＝减速斜率；瞬时值未允许）','',''),('8800','煞车盘动作未达标准','实际动作监视电路的响应',''),('89…','错误的操作码1、Byte：片段码高2、Byte：片段码低3、指令指示器高4、指令指示器低','伴随 56xx 后发生且连续储存 4 次。读取整段错误码包含潜码 xx，联络 VTS 或 QMS 部门','SM1'),('8A01','加速斜率','',''),('8A02','减速斜率','',''),('8A03','煞车作用时间','',''),('8A04','急拉（整体的）','',''),('8A05','1、急拉','',''),('8A06','2、急拉','',''),('8A07','3、急拉','',''),('8A08','4、急拉','',''),('8A09','加速斜率预先控制','',''),('8A0A','增益','',''),('8A0C','保养驾驶速度','',''),('8A0E','重拉水平速度','',''),('8A0F','上行强迫减速点','',''),('8A0b','额定速度','',''),('8A0d','调整运转速度','',''),('8A10','下行强迫减速点','',''),('8A11','着床速度','',''),('8A12','着床距离','',''),('8A…','参数设定超出 MW1 卡容许范围 错误仅发生于起始期间','',''),('9000','安全回路接通时速度＞0.5m/s','安全回路经 SR 模块接通且 CPU 检测速度＞0.5m/s。可能当错误的预先准备运转，在停滞时回授脉冲发电机仍有脉冲讯号','N2'),('9100','安全回路接通时车厢未在门区域位置','安全回路经 SR 模块接通且 CPU 未侦测到楼码片。可能原因：油压梯的上下变动；如果车厢停止在非门区域（如钢索打滑）或极限框架内','N2'),('9200','在停车或停滞状态时 V＞0.3m/s','脉冲发电机，特别形号 Wachendorf，在停滞状态仍有脉冲输出。更换 11.95 以后改良的脉冲发电机。自 TCI 工作版本 06.95 以后于停滞时速度不大于监视状态。','N6'),('9300','重拉水平速度＞0.2m/s ','在停车或停滞状态时重拉水平速度＞0.2m/s','N6'),('9400','速度监视装置跳脱','监视器反应在 V+10％；特殊工作作用也可能（10％限速器开关的替代）','SM1'),('9500','驱动监视装置的反应（16M，25M，API/CPI，使用 Beringer 可变速油压梯）','温度监视欠逆向监视参考/实际值监视（beringer）驱动控制器停止等API/CPI 参考参数输入器错误码','MN2'),('9900','MW1 速度监视','操作状态 00，01 或 04 速度＞0.3m/s 的错误','N1'),('9A00','安全回路经 SR 模块接通时 V＞0.5m/s 输入MW1','操作状态 03 速度＞0.5m/s 的错误 N19b00 保养驾驶速度监视 操作状态 07 速度＞0.63m/s（EN81）速度＞0.4m/s（Russia）的错误','N1'),('9E00','减速斜率监视第三轨，光栅装置','检查光栅','MS1'),('9F00','减速斜率监视第三轨，减速斜率监视跳脱','含缓冲器的高速电梯缓冲器降低','N1'),('C000|d000','接近停楼时加/减速斜率太陡','MD/MD1 加/减速斜率调整较平缓后 Techin','N1'),('C100|d100','改变装置反应','减速点太接近楼码确认勾。加/减速斜率调整较平缓后 Techin','N1'),('C200|d200','改变装置反应','加速顶点超出加速斜率范围。加/减速斜率调整较平缓后 Techin','N1'),('C300|d300','改变装置反应','参考/实际值偏差过大（电梯过快）加/减速斜率调整较平缓后 Techin','N1'),('C400|d400','改变装置反应','同 C300/d300','N1'),('C500|d500','MD/MD1－CPU 信号转换错误','加速顶点，减速点或停止点过头。脉冲发电机异常或打滑；调整加速斜率后 Tech-in','N1'),('C600|d600','MD/MD1－CPU 信号转换错误','车厢在两个门区域间。假设点在门最后离开的区域内。同 C500/d500','N1'),('C700|d700','MD/MD1－CPU 信号转换错误','路径实际值已校正。同 C500/d500','N1'),('C800|d800','如果 AF13＆AF20 在 Tech-in 模式中未写入，超过值的范围','执行 tech-in',''),('C900|D900','无运转操控','','N'),('CA00|dA00','无运转操控','','N'),('CAN事件来自 MC1/MC2/MC3界面（CANL＝车厢扁平电缆）','','',''),('CAN事件来自 MC3界面（C ANS＝坑道扁平电缆）','','',''),('CAN事件来自 MF3或 MF3D','','',''),('CAN事件来自 MZ1 关于坑道/车厢','','',''),('CAN事件来自 MZ1 关于车厢扁平电缆','','',''),('CAN－ MP 卡错误（0MP 上到 15MP）','','',''),('CC00|dC00','无运转操控','','N'),('CE00|dE00','无运转操控','','N'),('CPI 控制器内事件','','',''),('CPU-MW/MW1 联络','','',''),('Cb00|db00','无运转操控','','N'),('Cd00|dd00','无运转操控','','N'),('E000|E100','读取错误','CPU 的 EEPROM 有缺陷；重插 EEPROM；检查 5V 电压','SM1'),('E200','原先的 BBC 和备份检查不正确','重插 EEPROM；重新 tech-in','SM1'),('E300','原先的 BBC 和备份检查正确但不同','重插 EEPROM；重新 tech-in','SM1'),('E400','记忆装置错误','CPU 的 RAM 异常',''),('E500','备份 BBC 错误','',''),('E600','原本 BBC 错误','',''),('E700','RAM 错误','','N1'),('E800','最上停层','两停楼电梯的保养平台展开','S1'),('E801','最上停层为 0','重作 AF10；停层数（包含假停层）必须储存于特别程序内','S1'),('E900','溢出错误 AF71（强迫减速）或','AF74（超速保护）的计算导致内存位置溢出','S1'),('EAxx','MC3：不明错误 xx 到外围装置','',''),('EEyy|EExx','EEPROM 内存储器位置 xxyy 异常','更新 EEPROM',''),('F000','CPU 与 MZ1 的传输错误','0C01，C02，C03，C10，C11，0C12 导致跳脱','MS1'),('F100','MZ1 与车厢板 MF3/MF4 等的传输错误','0C04，C09，0C0A，0C0b，0C0C 导致跳脱','MS1'),('F200','MZ1 与车厢附属装置如 LSM1，F2 等的传输错误','0C0d，0C0E 导致跳脱','MS1'),('F300','MZ1 与机房扁平电缆如 MP 卡等传输错误','0C05，0C06，0C07，0C08 导致跳脱','MS1'),('F400','0C…错误引起的停止','F000 到 F300 未包含','MS1'),('F800','8kRAM/EEPROM 未侦测到','较早的错误 0203 或 0204','MS1'),('FE00','MC1：快闪数据错误（BBC 检查总和）','Tech-in 数据流失；重新 tech-in','MS1'),('Fb00','远程电话服务码','远程电话服务装置一般讯息（未包含在TCI/TCM 错误表内）',''),('Fd00','MC1：快闪数据错误（BBC 检查总和）','Tech-in 数据在 RAM 复制范围内',''),('Fd01','MC1：RAM 复制数据错误','Tech-in 资料愉闪存内 OK',''),('Fd0F','快闪数据错误','于特殊程序数据范围内的错误',''),('FdFA','特殊命令 EPROM 未作用','电梯特殊程序未被加载',''),('MC 的处理器缺失（CPU E60）','','',''),('MC1/MC2 的处理器缺失（CPU）','','',''),('MC1/MC2/MC3','','',''),('MD/MD1 与 CPU 间正确顺序检查码运转方向：C?00＝下行方向／d？00＝上行方向','','',''),('MH3 事件','','',''),('MM－ME 事件','','',''),('MQ 卡','','',''),('MQ1 事件','','',''),('MZ/MZ1','','',''),('MZ1/CPU','','',''),('TCI/TCM 一般性错误','','',''),('TCI/TCM 控制盘错误','','',''),('TCI/TCM 错误','','',''),('TCM 控制-MD1 卡运转方向：C?00＝下行方向／d？00＝上行方向','','',''),('TCM 控制系统的错误','','',''),('TCM－API 的 FIS 接口（在 API 控制器内）','','',''),('b000','操作状态错误','选择器无法辨识正确的操作状态','N3'),('一般性错误','','',''),('主门驱动','','',''),('使用 CPU（E60）的 TCM（CAN）运行控制的错误','','',''),('使用 MC1 卡 CPU 的错误','','',''),('使用 MC1 错误码 2C00 到 2F00 包含子码位置 XX','','',''),('使用目标选择控制（DCS）TCM的错误','','',''),('副门驱动','','',''),('参考-实际值监视','','',''),('安全回路','','',''),('无机房电梯','','',''),('自 12.08.96 版本以后 TCI/TCM 新增错误码','','',''),('错误码','错误说明','原因及修理指南','备注')"
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    return render_template('add_data.html')
@app.route('/sql/insert/hitachi_mca')
def insert_tab2():
    cur, conn=Conn.conn()
    sql=f"INSERT INTO `hitachi_mca` VALUES ('10','电路标准电压异','电路标准电压异常'),('11','  #50B ON 故障',''),('12','  #5    ON 故障','副微机停机'),('13','安全回路动作故','综合微机与副微机通信'),('14','软件WDT 动作检','双重输入缓冲器故障'),('15','      VR1 P48V 电源','  INV 输出封锁电路 OFF'),('16','检修运行输入信',''),('17','号机 NO.异常',''),('18','连续 3 次开门锁','  #50B    ON 故障'),('19','   ，ORS 经',''),('1A','  40D OFF 故障','＃ 15B    ON 故障'),('42','  40G ON 故障','      50B       OFF 故障'),('43','  40D ON 故障','   SDS1 同时 ON 故障'),('44','  #5    OFF 故障','   15B    OFF  故障'),('45','  #5R OFF 故障','滑轮滑动检测'),('46','运行指令输入缓',''),('48','连续 3 次开门不成功','电流不足检出'),('62','门机电源切断无效故','速度偏差异常'),('80','   FMLX 、FMLY 、#100RXA 、B OFF 故',''),('81','  门机电源 OFF 故障',''),('82','  开关门堵死故障',''),('83','   FMLX 、ON 故障检出',''),('84','   FMLY    ON 故障检出',''),('90','    SCLB3 板通信故障','负荷检测电路异常'),('92','  综合微机重启多次所导致的最近楼层',''),('93','  散热片过热保护动作','  SDS 不动作(SDS ON 故'),('96','   ROM 和数错误 1','过电压发生次数 10 次'),('97','   ROM 和数错误','现场调整区规格表和数'),('9D','  旋转编码器断线，逆相故障','  CNV 侧 霍尔 CT 故障'),('A0','逆转检出','DZA 位置检测器 OPEN'),('A1','  旋转编码器磁极位置异常','DZB 位置检测器 OPEN'),('A6','   ALP 异常',''),('A7','   #5R OFF 故障','多次自救检出'),('A9','   #40D 接触器故障','  SDS 强制减速开关多次'),('AE','  开门锁死导致运行至其他层 (1 回)',''),('AF','  光幕异常',''),('B0','变频门机故障',''),('B1','变频门机微机死机故障',''),('C0','群管理-号机通信故障',''),('C2','待机系微机异常',''),('C3','运行系微机异常',''),('C4','共通厅外召唤回路异常',''),('C5','群管理微机死机',''),('C6','单梯厅外召唤回路异常',''),('C9','   FMLX OFF 故障检出',''),('CA','   FMLY OFF 故障检出',''),('CB','   #100RXA 、B OFF 故障检出',''),('D1','   CLS 、OLS 同时 ON 故障','转矩测定运行异常'),('D7','曾经发生开门或关门锁死故','过电压发生次数 5 次以上'),('D8','开门时 ORS 连续动作故障',''),('D9','关门时 ORS 连续动作故障',''),('E3','   SCLB3 板通信故障(预报)',''),('EF','工程用层高测定规格表 ON','   SDS  速度异常 1')"
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
    return render_template('add_data.html')
@app.route('/sql/Oinsert')
def one_insert():
    cur, conn=Conn.conn()
    sql=f"INSERT INTO `thyssenkrupp` VALUES ('01XX','停楼 XX 的 RK 或 RKD 未接通','检查停楼 XX 的 RK 接点或机械部分','6'),('0201','禁止叫车经由监视程序','CPU 上一只 8K-RAM 被命令指示','1'),('0202','类似 ZSE 在特殊程序被释放，仅 SiemensCPU','使用包含电池组 RAM 芯片的 Thyssen CPU（位置记忆如果发生电源异常或 HS 关闭）','1'),('0203','TCM 控制',' 8K-RAM 无法认定；F800 伴随发生','1'),('0204','TCM 控制',' 8K-EPROM 无法认定；F800 伴随发生','1'),('0280','不明确或错误操作状态','','1'),('0301','特殊程序中未规定恰当的隔离停楼','隔离停楼未定义（检查数据页）或错误的特殊程序 EPROM','1'),('0302','特殊程序中未规定恰当的停靠停楼','停靠停楼未定义（检查数据页）或错误的特殊程序 EPROM',''),('0303','特殊程序中未规定恰当的火警停靠停楼','火警停靠停楼未定义（检查数据页）或错误的特殊程序 EPROM',''),('04NN','TCI：磁簧开关 ZSE 引起的错误','一个以上的 ZSE 开关导通，电梯将被停止，错误码 04NN 连续纪录 4 次。检查 ZSE 开关','SM3'),('04XX','TCM：磁簧开关 ZSE 引起的错误','一个以上的 ZSE 开关导通，所有激磁的停楼ZSE 将被显示。检查 ZSE 开关',''),('0542','群控的电梯数或停楼数不可接受','',''),('0553','传输运转在错误的群控状态；05XX 随后发生','缺乏 XX 号电梯群控连接',''),('05A0','群控通讯协议不相容','群内所有电梯 MZ1 卡使用相同版本',''),('05A8','群控通讯协议与群控处理器不兼容','检查 MZ1 卡传输版本和群控处理器',''),('05C ','的地叫车未服务','叫车已分配但指定电梯未服务',''),('05C0','特殊程序复归运作','暂停时间到而复归',''),('05XX','TCM 群控特殊程序错误信息。出现在下列的错误指示之后','询问 TU 或 VTS 在这些错误发生时。XX＝详细错误叙述数据',''),('05YY','群控命令错误（有缺陷的 MG 卡或群控接线失败）','TCI：检查 MG 卡或群控接线TCM：检查群控扁平电缆（MZ1 卡）软件错误：确认工作程序版本','2'),('05b0','DCS 重置：05XX 伴随发生ZES＝目标输入终端机','ZES 维持执行。检查电压供应及 CAN 与各ZSE 的连接XX＝相对应停楼',''),('05b1','来自 DCS 不明的回应：Hallo(=起始程序)05XX伴随发生','XX＝相对应停楼',''),('05b2','DCS 发出不明的准备好的讯息（＝起始终结）05XX伴随发生','XX＝相对应停楼',''),('05b3','DCS 起始值暂停，程序数据开端，05XX 伴随发生','起始 DSC 失败，检查电压及连接个别 ZSE 的讯号传输线XX＝相对应停楼',''),('05b4','DCS 默认值暂停，程序数据末端，05XX 伴随发生','',''),('05b5','DSC-电梯动作暂停，05XX 伴随发生','无来自 DSC 周期性响应，检查电压及连接个别 ZSE 的讯号传输线XX＝相对应停楼',''),('06XX','停楼 XX 闭锁失败 3 次导致紧急停止','检查停楼XX闭锁开关或机械部分','M2'),('0701','主门 TSO 错误：TO 命令输出 30 秒而 TSO无讯号。CPU 在到时间后将仿真 TSO 讯号，使门能恢复正常动作','TSO 缺陷或调整不良。有闭锁装置的电梯门，不闭锁异常可能因门控制系统无法执行 TO 命令',''),('0702','主门 TSO 错误（参考 0b04）','TK 导通而 TSO 显示主门开启。重置引起 N1',''),('0801','副门 TSOD 错误','参考 0701','1'),('0802','副门 TSOD 错误','参考 0702','N3'),('09NN','叫车或命令已存在，但电梯仍停留在某一楼层超过 4min 没有动作','可能门再开装置造成，参考 0500 功能 0d 栏。有反旋装置之油压梯，可能因车厢过低或限速器张力轮不顺而引起（参考后面范例）','M3'),('0A2F','钢索松弛','',''),('0A30','磨到外门区域','',''),('0A31','车厢门未关','',''),('0A32','停楼外门未闭锁','',''),('0A33','油温超过 70℃','',''),('0A34','油平面监视','',''),('0A46','保养开关 ON','',''),('0A47','保养开关 OFF','',''),('0AAA/0AXX','特殊程序错误Tech-in 错误（主边升降道 Tech-in；0bXX 副边升降道）参考工作 Tech-in 通告（MA 13 6510.046）','可能比对命令程序操作错误。AA＝表列叙述错误（操作错误说明）如果错误发生于 Tech-in AF0D 或 AF0C，0AXX 表示停楼 XX 的 MS2 未被分派','2'),('0C01','CPU：MZ1 到操作系统失败','CPU 到 MZ 传输的问题','S1'),('0C02','CPU：MZ1 到操作系统失败','CPU 到 MZ 传输的问题','S1'),('0C03','CPU：MZ1 到操作系统失败','','S1'),('0C04','CPU：车厢的开始值≠参考值','a)电梯特殊程序不符b)传输扁平电缆接触不良检查电梯特殊程序 EPROM（地址）',''),('0C05','CPU：MP 的开始值 1≠参考值 1','a)MP 卡不正常b)MP 卡指拨开关编码不正确c)扁平电缆联络异常检查电梯特殊程序 EPROM（地址）',''),('0C06','CPU：MP 的开始值 2≠参考值 2','a)MP 卡不正常b)MP 卡指拨开关编码不正确c)扁平电缆联络异常检查电梯特殊程序 EPROM（地址）',''),('0C07','CPU：机房扁平电缆开始值 1≠参考值 1','参考上列 a)及 c)',''),('0C08','CPU：机房扁平电缆开始值 2≠参考值 2','参考上列 a)及 c)',''),('0C09','CPU：MF4 的开始值 1≠参考值 1','MF4 卡正常，但没有来自 MF4 的确认接收讯号',''),('0C0A','CPU：MF4 的开始值 2≠参考值 2','MF4 卡正常，但没有来自 MF4 的确认接收讯号',''),('0C0C','CPU：MF4 的开始值 4≠参考值 4','MF4 卡正常，但没有来自 MF4 的确认接收讯号',''),('0C0E','CPU：FKZ 的开始值 2≠参考值 2','FKZ＝车厢附件（如门系统、启动补偿装置）',''),('0C0b','CPU：MF4 的开始值 3≠参考值 3','MF4 卡正常，但没有来自 MF4 的确认接收讯号',''),('0C0d','CPU：FKZ 的开始值 1≠参考值 1','FKZ＝车厢附件（如门系统、启动补偿装置）',''),('0C10','CPU：MZ1 的默认值计时错误','没有来自 MZ1 的确认接收讯号','S1'),('0C11','CPU：MZ1 的默认值计时错误','起始及完成接收皆未被确认','S1'),('0C12','CPU：MZ1 的默认值计时错误','起始及完成接收确认超过 20 秒','S1'),('0C13','CPU：MZ1 确认标准重置','MZ1 错误，使用 V10 以后程序','N1'),('0C1C','CPU：无 CPI 联络讯号','F31C 伴随发生',''),('0C20','MZ1：坑道缓冲区过载','坑道/车厢数据无法读取。可能 MZ1、坑道、车厢传输线接头不良',''),('0C21','MZ1：坑道缓冲区过载','坑道/车厢数据无法读取。可能 MZ1、坑道、车厢传输线接头不良',''),('0C22','MZ1：坑道缓冲区过载','坑道/车厢数据无法读取。可能 MZ1、坑道、车厢传输线接头不良',''),('0C23','MZ1：坑道缓冲区过载','坑道/车厢数据无法读取。可能 MZ1、坑道、车厢传输线接头不良',''),('0C24','MZ1：坑道缓冲区过载','坑道/车厢数据无法读取。可能 MZ1、坑道、车厢传输线接头不良',''),('0C25','MZ1：坑道缓冲区过载','坑道/车厢数据无法读取。可能 MZ1、坑道、车厢传输线接头不良',''),('0C30','MZ1：坑道扁平电缆有缺失','重新起始超过 MZ1 限制','N1'),('0C31','MZ1：坑道扁平电缆传输错误','MZ1 对坑道检测错误',''),('0C32','MZ1：坑道扁平电缆资料过载','',''),('0C3A','MZ1：MF3D 传输程序流失','',''),('0C3C','MZ1：MF3 回应缺失','MZ1 到车厢传输线端子不良',''),('0C3b','MZ1：MF3 传输程序流失','',''),('0C3d','MZ1：MF3 回应缺失','MZ1 到车厢传输线端子不良',''),('0C40','MZ1：车厢缓冲区过载','已读取超出 MF1 能处理的数据量',''),('0C42','MZ1：车厢缓冲区过载','已读取超出 MF1 能处理的数据量',''),('0C43','MZ1：车厢缓冲区过载','已读取超出 MF1 能处理的数据量',''),('0C45','MZ1：车厢缓冲区过载','已读取超出 MF1 能处理的数据量',''),('0C50','MZ1：车厢扁平电缆缺陷','重新起始超过 MZ1 限制',''),('0C51','MZ1：车厢扁平电缆传输错误','重新起始超过 MZ1 限制',''),('0C52','MZ1：车厢扁平电缆资料过载','重新起始超过 MZ1 限制',''),('0C53','MZ1：车厢扁平电缆要求重置','重新起始超过 MZ1 限制',''),('0C60','MZ1：频率分配异常','CAN 测试',''),('0C70','CANL 测试：频率分配异常','CAN 控制器被初始化',''),('0C73','CANL 测试：CAN 控制器要求重置','CAN 控制器被初始化',''),('0C74','CANL 测试：登录状态错误（EMC）','CAN 控制器被初始化',''),('0C75','CANL 测试：输出缓冲区过载','',''),('0C76','CANL 测试：输出缓冲区过载','',''),('0C78','CANS 测试：频率分配异常','CAN 控制器被初始化',''),('0C7A','CANS 测试：坑道资料过载','',''),('0C7C','CANS 测试：登录状态错误（EMC）','',''),('0C7b','CANS 测试：坑道扁平电缆重置请求','CAN 控制器被初始化',''),('0C80','MF3：MF3 重置','',''),('0C81','MF3：MZ1 传输程序失效','',''),('0C85','MF3：坑道资料过载','超过 MF3 能处理数据',''),('0C86','MF3：坑道扁平电缆传输错误','MF3－CAN 传输缺失记录',''),('0C87','MF3：坑道扁平电缆缺失','',''),('0C88','MF3：确认使用 MF2 不允许','＞56HS 使用 MF2；检查',''),('0C89','MF3：CAN 芯片异常','要求或频率重置',''),('0C8A','MF3：MF3 起始错误','',''),('0CA0','MF3D：MF3 重置','',''),('0CA1','MF3D：MZ1 传输程序失效','',''),('0CA5','MF3D：坑道资料过载','超过 MF3D 能处理数据',''),('0CA6','MF3D：坑道扁平电缆传输错误','MF3D- CAN 传输缺失记录',''),('0CA7','MF3D：坑道扁平电缆缺失','',''),('0CA8','MF3D：确认使用 MF2 不允许','＞56HS 使用 MF2；检查',''),('0CA9','MF3D：CAN 芯片异常','要求或频率重置',''),('0CAA','MF3D：MF3 起始错误','',''),('0CE0','重置','',''),('0CE2','内存数据过载','',''),('0CE3','扁平电缆错误','',''),('0CE4','扁平电缆干扰','',''),('0CE5','不完整的传输数据','',''),('0CE8','运转时间错误','',''),('0CE9','监视器','',''),('0CEA','过电流','',''),('0CEC','过热-散热片','',''),('0CEE','限速器无作用','',''),('0CEF','F2/1：热耦室','',''),('0CEb','过电压','',''),('0CEd','过热-门马达','',''),('0CFF','CPU：来自 MZ1 不明确命令','如此错误发生，参考内存位置 dE2F 及 dE3F并连同错误的卡片寄给 VTS 或 QMS 部门注意：重置将会清除指定的内存位置',''),('0Cd0','重置','',''),('0Cd2','内存数据过载','',''),('0Cd3','扁平电缆错误','',''),('0Cd4','扁平电缆干扰','',''),('0Cd5','不完整的传输数据','',''),('0Cd8','运转时间错误','',''),('0Cd9','监视器','',''),('0CdA','过电流','',''),('0CdC','过热-散热片','',''),('0CdE','控制器无作用','',''),('0CdF','F2/1：热耦室','',''),('0Cdb','过电压','',''),('0Cdd','过热-门马达','',''),('0E00','从 MW1 到 CPU 传输缺失','','1'),('0F0A','设置旗标开关 ON','开关位于 MZ 或 MZ1 上',''),('0F0C','电话程序设置旗标','服务状态开关 ON',''),('0F0E','设置旗标开关 OFF','开关位于 MZ 或 MZ1 上',''),('0F0F','电梯功能开启','保养平台关闭','Reset'),('0F0b','无机房电梯','保养平台开启 Reset',''),('0F0d','电话程序设置旗标','服务状态开关 OFF',''),('0FZZ','设置旗标','ZZ＝旗标编号',''),('0b01','主门光栅错误','光栅遮断超过 EPROM 特别程序规定时间；预防 0900 产生（错误可能发生在分离控制＆光栅＆TCI 版本 06.95 以上）','M2'),('0b02','副门光栅错误','参考 0b01','M2'),('0b03','群控失败超过1小时','电梯脱离群控。例如专用、被占用等（软件错误；使用 TCI 自 06.95 的工作版本）','M2'),('0b04','TSO 错误－主门','虽然门关闭，但 TSO 表示门开启','SM2'),('0b05','TSOD 错误－副门','虽然门关闭，但 TSO 表示门开启','SM2'),('0b06','地震感知器动作','仅使用 MCX CPU','SM1'),('0b07','车厢保养驾驶输入到 MF3 讯号不良','仅使用 MCX CPU（自工作版本 V51＆V81）',''),('0d1b','监视 MW1 参考-实际值（B＝运转状态）','缺少脉冲讯号（仅在保养运转状态）；CPU 检出缺乏脉冲','N'),('0d2b','脉冲顺序监视：上行时 A 频在 B 频之前','脉冲频 A＆B 被拌和。正确的脉冲顺序显示于 ESA 卡（Iso60）或 NIM 卡（Iso25M）','N'),('0d3b','实际值＞参考值（+10﹪在 VN；+100﹪在VI；+80﹪在 VJ；+50﹪在 VNS）','如果紧急停止的参考值已经到 0 而实际值仍在运行','N'),('0d4b','实际值＜参考值（-10﹪在 VN；-100﹪在 VI；-80﹪在 VJ；-50﹪在 VNS）','错误可能发生在：门闭锁开关不良（没有14XX），缺乏脉冲讯号，MW1 参考值电压＞9.8V，加速斜率设定太陡峭（实际值无法达成），驱动控制器太迟钝；I 成分设定过高等因素','N'),('0d5b','实际值＞参考值','实际值＞额定+10﹪','N'),('0d6b','驱动侧控制器停止（仅在模拟控制器如Iso25M）','设定驱动包含控制范围（非数字控制）加速设定太陡峭，马达开关设定不适当，齿轮油太冷','N'),('0d7b','回授参考值（MW1）计算未水平','虽车厢位于水平位置，但 MW1 计算值未达水平＞3 ㎜此错误讯息可能产生。（12.95 以上软件错误码）','N'),('0d8b','回授参考值（MW1）停滞速度＞0.25m/s','MW1 表示停滞速度＞0.25m/s。原因：在停滞速度脉冲发电机仍产生脉冲；脉冲信号线（隔离线）有干扰信号','N'),('10YY','CPU 卡缺失','Reset 将伴随发生','N'),('1101','TCM：群控的 CAN 扁平电缆缺失','MZ1 上群控 CAN 扁平电缆失误。使用包含群控 CAN 扁平电缆的 MZ1',''),('11YY','MG 卡缺失','群控输入/输出芯片失效','1'),('12XX','计算位置不等于车厢实际位置','非 LK 错误。楼层计算程序在停车状态的错误','3'),('13XX','被裁定的位置不等于车厢实际位置','参考 12XX','3'),('14XX','停楼 XX 闭锁开关 RK 打开','RK 开关在运转期间被打开。原因：外门用钥匙开启；TSM 或闭锁磁铁动作不完整；凸轮马达调整不当；凸轮或闭锁凸轮在 by-passing时摩擦','N8'),('15XX','计算位置不等于实际位置','楼层计算程序在停滞起动前状态的错误','2'),('16YY','MW/MW1：位置差异','仅发生在有 MW/MW1 的电梯','3'),('17YY','CPU－MW/MW1 错误','仅发生在有 MW/MW1 的电梯（储存过满）','N1'),('18XX','停楼 XX 副门闭锁开关 RKD 打开','参考 14XX','N8'),('19NN','门区域未被认可（CPU 无法辨识楼码片，但已开始着床）','在停车状态 LK 到门区域信号失效。对应到功能 0500，05 列说明（参考后面范例）','N2'),('1AYY','LK 检测器检出错误：应暗实际亮','可能发生错误：LK 或楼码片的问题；钢索打滑或控制器不稳定；回授有缺陷。','N8'),('1CNN','不明确的运转','已起动运转但无有效命令','4'),('1ENN','在 bypassing 记号最终停楼楼码片或保养驾驶限制开关 IFO/IFU 无延迟','车厢位置 Bit20 在 25 之上；Bit26（1）被激磁；Bit27（1）被激磁。NN 是 16 进位表示（参考后面范例）','3'),('1F00','机房扁平电缆中断','',''),('1F01','机房扁平电缆错误','',''),('1F02','机房扁平电缆过载','',''),('1F03','输入缓冲区过载','',''),('1F04','电路板过载（reset）','',''),('1F05','无交握传输程序 交握是定义如两块数据电路板周期性数据交换','',''),('1F80','机房扁平电缆被中断','',''),('1F81','机房扁平电缆错误','',''),('1F82','机房扁平电缆过载','',''),('1F83','输入缓冲区过载','',''),('1F84','FIS：重置','紧急停止或电源重置将被触发（MC1）','N1'),('1F85','FIS：外在的接触器交握程序 2X 失误','',''),('1F86','FIS：外在的周期性传输程序接触器失败','','N1'),('1F87','FIS：内部的错误','',''),('1F88','MM/ME：机房扁平电缆被中断','',''),('1F89','MM/ME：机房扁平电缆错误','',''),('1F8A','MM/ME：机房扁平电缆过载','',''),('1F8C','MM/ME：重置','',''),('1F8E','MM/ME：MM 或 ME 被 MCx 起始','',''),('1F8F','MM/ME：因 MM 或 ME 而重置','',''),('1F8b','MM/ME：输入缓冲区过载','',''),('1F8d','MM/ME：无传输程序交握','',''),('1F90','MQ1：机房扁平电缆被中断','',''),('1F91','MQ1：机房扁平电缆错误','',''),('1F92','MQ1：机房扁平电缆过载','',''),('1F93','MQ1：输入缓冲区过载','',''),('1F94','MQ1：重置','',''),('1FA0','MH3：机房扁平电缆被中断','',''),('1FA1','MH3：机房扁平电缆错误','',''),('1FA2','MH3：机房扁平电缆过载','',''),('1FA3','MH3：输入缓冲区过载','',''),('1FA4','MH3：重置','',''),('1FA5','MH3：来自 MH3，两个交握错误','',''),('1FA6','MH3：控制器到 MC1/MC3 的周期性传输程序失败','',''),('1FA7','MH3：MH3 卡内部错误','',''),('1FA8','MH3：安全状况后重置','',''),('1bYY','LK 检测器检出错误：应亮实际暗','可能发生错误：LK 或楼码片的问题；钢索打滑或控制器不稳定；回授有缺陷。','N5'),('1dYY','紧急停止（错误的运转命令）','无或两方向运转命令产生','N3'),('20TT','SR 模块错误','SR 作用时，侦测 SR 回到 CPU 讯号时间。TT＝16 进位数字乘以 50ms。同错误码 2300',''),('2100','EEPROM 错误（28C64 芯片）','EEPROM 内存储器位置缺陷','S1'),('2200','SR 模块错误（分辨率＞100ms）','经由 CPU 通道 I 中断 100ms 后，侦测 SR 回到 CPU 讯号仍存在','N4'),('2300','SR 模块错误','与错误码 4300 同，但不会停止（德国不允许）','8'),('2400','CPU：EEPROM 缺陷','EEPROM 内存储器位置缺陷。重插 EEPROM 或 CPU SM3按钮检查',''),('2502','外叫车缺陷','主门侧外叫车下行不良',''),('2504','外叫车缺陷','主门侧外叫车上行不良',''),('2520','外叫车缺陷','副门侧外叫车下行不良',''),('2540','外叫车缺陷','副门侧外叫车上行不良',''),('2604','保养平台开启同时极限开关闭路','极限开关被短路或保养平台输入讯号不良。无运转命令的可能；除了车厢保养外电梯将停止运转。错误信息于 3 秒后产生','MS'),('2605','保养平台关闭，极限开关既不开也不关','极限开关和配重冲突或极限开关正被 closed;仅紧急运转下行可允许。错误信息于 3 秒后产生','MS'),('2606','保养平台开启，极限开关既不开也不关','过渡状态，极限开关 open 或不良；无运转命令的可能。除了车厢保养外电梯将停止运转。','MS'),('2607','保养平台开启，极限开关既开又关','开关不良，无运转命令的可能。电梯将停止运转。错误信息于 3 秒后产生','MS'),('2608','保养平台开启，极限开关既开又关','开关不良，无运转命令的可能。电梯将停止运转。错误信息于 3 秒后产生','MS'),('2609','无机房电梯','尽管电梯正常运作，SR 模块复检功能动作','MS'),('260A','无机房电梯','如果最上停楼未到达（极限开关动作）SR 模块复检功能缺失',''),('27XX','仅发生在使用MC1 或MC2 的TCM 电梯（XX＝意义参考补充说明版本 MA12 6510.062）','监视输入或 RFS 模块（relay flat pit）不良','MS'),('2800','低负载运转期间失败','','N'),('284X','低负载运转时间超过 30 秒','','N'),('288X','低负载运转上行时间超过 30 秒','','N'),('2900','虽然安全回路打开，但车厢盖板合拢','','MS'),('2910','连续 3 次低负荷运转失败','','MS'),('29XX','车厢盖板不良','','MS'),('2A00','TMI 接触器确认','新－旧：00 00',''),('2A11','TMI 接触器确认','新－旧：01 01',''),('2A12','TMI 接触器确认','新－旧：01 10',''),('2A20','TMI 接触器确认','新－旧：10 00',''),('2A21','TMI 接触器确认','新－旧：10 01',''),('2A22','TMI 接触器确认','新－旧：10 10',''),('2A32','TMI 接触器确认','新－旧：11 10',''),('2A33','TMI 接触器确认','新－旧：11 11',''),('2C00','变动检查错误（LK/LN 于重拉水平）','LK＆LN 检测将重拉水平状态。不允许向上时 LK 亮 LN 暗；向下时 LK 暗 LN 亮。原因：过度的重拉水平速度；LK/LN 间距太小（如果调整需重新 Tech-in）','5'),('2E00','重拉水平时间＞7S（自工作版本 02.96/26 增加到≦20S）','重拉水平速度太慢；油压梯基本容积设定错误，致使车厢开始移动时间过长','N2'),('2F00','重拉水平距离＞4 倍重新起动单位','使用标准楼码片 4 倍重新起动单位＝8 ㎝','N1'),('2b00','在停滞操作状态开始闭锁超过 60 秒','',''),('2d00','SR 模块异常','重拉水平期间到 CPU 检查讯号异常。检查区域开关 ZS、检查 KTK','N2'),('3000','LK 读取错误（调整运转期间紧急停止）','调整运转期间楼码无法辨识。需坑道资料Tech-in','N2'),('3100','LK 错误','检查 LK',''),('3200','LK 错误','检查 LK',''),('3300','LK 错误','检查 LK',''),('3400','LK 错误','检查 LK',''),('3500','激磁选择器错误','楼码片出发勾无法辨识（检查 LK）','2'),('3600','激磁选择器错误','水平窗口感测是暗的（检查 LK 和楼码-含磁簧近接开关选择器）','2'),('3700','激磁选择器错误','在停止操作状态 ZSE 未激磁','2'),('3C00','LK 错误（读取错误）','楼码与 Tech-in 时读入楼码不符，仅着床时会紧急停止。原因：LK 传感器跳动；牵引力太低（主钢索打滑）；回授发电机打滑（油压梯）；LK 脉冲线不良；楼码片脏','N4'),('3E00','防旋装置异常（限速器起动）','MAS 电磁动作但限速器上开关开启失败。原因：限速器上开关故障；限速器上闭锁爪卡住（如果合闸杆停止在棘轮上，电磁冲程相对小）。校正：放置两只垫圈（6 ㎜）于电磁和固定架间','SM3'),('3F00','防旋装置异常（限速器抑制）','电磁被释放但开关打开失败。原因：开关故障；计时模块 ZSP 接触器设定太久，限速器模块失败','SM3'),('3b00','楼码水平窗口错误','',''),('3d00','LK 错误（楼码片）','抵达码不等于出发码（仅发生于 by-passing）',''),('4000','警铃动作','特殊工作程序动作',''),('4100','运转监视装置缺失（缺少脉冲讯号）','CPU 的运转监视装置中断（牵引式电梯缺少脉冲＞4S 或油压电梯＞8S）。原因：脉冲发电机故障；油压梯基本容积设定错误','SM1'),('4200','运转时间监视','在着床及调整运转速度时间太久：LK 无明暗变化 VN＞20s VJ＞45s','SM3'),('4300','SR 模块异常（闭锁开关未桥接）','CPU 检查缺失。原因:SR 模块异常，ZS 开关不良，ZSE 及 LK 进入楼码片透入深度不正确','SM8'),('4400','SR 模块异常（仅油压梯最低楼层停止）','如发生于较高楼层同 4300；如仅发生于最低楼层原因：错误发生于油压梯，一个回归最低楼层错误必伴随发生','SM2'),('4500','紧急停止按钮被执行','仅挪威版中（参考数据图表）','N'),('4600','维修保养开关 ON','仅顾客特殊功能有效',''),('4700','维修保养开关 OFF','仅顾客特殊功能有效',''),('4800','重新准备好讯息','电梯重新准备好自发的讯息','N'),('4900','调整运转状态超过内定值（5min）','检查调整运转时间为何无法于 5min 内完成','M2'),('4A00','CPU 与 MW/MW1 间传输错误','MW/MW1 卡在较高质量装置缺失','N2'),('4C00','MW/MW1：在测试模式','MW/MW1 卡上 S9 接通',''),('4E00','路径计算器 MW/MW1：','到路径计算器传输（RST5.5）缺失',''),('4F00','到 CPU 的接触器检查回报（设定值与实际值比较电路接触器）','在调整运转或尝试数次调整运转时接触器检出错误','SM2'),('4b00','MW/MW1：计算位置不等于实际位置','MW/MW1 辨识确认勾缺失。原因：正常运转伴随紧急停止运转（非调整运转）','N2'),('4d00','MW/MW1：未准备完成','MW/MW1 自 CPU 重置','N2'),('5000','停止带有还原及 TCM 控制的集体错误','原因：TCM 错误 C01，C02，C03，C04，C11，C12 发生（初始值的问题）','SM2'),('5100','运转监视','缺少脉冲讯号＞4S','N2'),('5200','紧急停止后调整运转','紧急停止后无重置的调整运转',''),('5300','随调整运转之后的运行','随调整运转之后的运行（紧急停止）',''),('5400','CPU 缺失（监视中断）','CPU 计算器缺失',''),('5500','重置','重置导因于程序重新起动（主电源 OFF/ON或电源供应中断）原因：％V 电压设定不正确；电源供应不稳定等',''),('5501','MC2 群控重置','DC24V 被断线',''),('5600','CPU 缺失（TRAP）','',''),('5600','分配错误致使中断执行','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('5601','记录轨迹中断','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('5602','非可遮蔽的中断','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('5603','断点中断','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('5604','INT（断路器）0 检测过剩致使中断执行','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('5605','系统限制，中断执行','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('5606','未使用的输出码（opcode）致使中断执行（X)错误 8900 将伴随发生','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('5607','漏失输出码（opcode）致使中断执行','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('5608','定时器 0 中断','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('5609','AMD 备份中断','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('560A','DMA（直间储存器地址）0 或 INT 5','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('560C','INT 0','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('560E','INT 2','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('560F','INT 3','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('560b','DMA 1 或 INT 6','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('560d','INT 1','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('5610','INT 4','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('5611','不同步串行埠 0 中断','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('5612','定时器 1 中断','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('5613','定时器 2 中断','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('5614','不同步串行埠 1 中断','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('56FF','不明确的软件中断（5620 到 56FF）','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS',''),('56…','不明确的中断','注意！！错误码 5600 到 56FF 处理器缺失讯息累加到数据表。替换 CPU 及数据部门 VTS 或 QMS','N'),('5700','调整运转','紧急停止及上述的错误后致使进入调整运转',''),('5800','紧急停止','某些错误后紧急停止',''),('5900','正停止于紧急停止事件中','如果特殊程序中的错误导致紧急停止发生时，电梯将被停止。地址码：A570 到 A57F（16 个错误能被写入；对照第 3 部分内存位置）','SM1'),('5A00','CPU-MW/MW1 错误','MW/MW1：信号准备好的缺失','SM2'),('5C00','CPU-MW/MW1 错误','MW/MW1：传输后无读取埠中断','SM2'),('5E00','CPU-MW/MW1 错误','MW/MW1：二次不明传输（无重复）','SM2'),('5F00','EK 错误（EK＝极限开关接触器）','EK 错误后将停止于最低停楼','MB'),('5b00','CPU-MW/MW1 错误','MW/MW1：TCI 重置后请求传输程序缺失','SM2'),('5d00','CPU-MW/MW1 错误','MW/MW1：一次不明传输（重复）',''),('6000','安全回路','EK 开路运转期间 EK 中断（不含调整运转）。在一些装置如 Isostop60（API）中，因驱动监视接触器于 EK 前，故释放时也会发生','MN'),('6100','安全回路','HK 开路 紧急停止或安全钳开关开路','N'),('6200','安全回路','TK 开路 内门开关 KTK 或 KTKD 于运转期间中断','N'),('6300','安全回路','KT 开路 闭锁开关 RK 或 RKD 于运转期间中断','N'),('6400','主机马达热藕开关中断','检查 PTC 热藕开关或 PTC 热藕接触器端子','MN'),('6500','00-00 0','接触器放开1 接触器吸上',''),('6600','00-01','0 接触器放开1 接触器吸上',''),('6700','00-10','0 接触器放开1 接触器吸上',''),('6800','00-11','0 接触器放开1 接触器吸上',''),('6900','01-00','0 接触器放开1 接触器吸上',''),('6A00','01-01','0 接触器放开1 接触器吸上',''),('6C00','01-11','0 接触器放开1 接触器吸上',''),('6E00','10-01','0 接触器放开1 接触器吸上',''),('6F00','10-10','0 接触器放开1 接触器吸上',''),('6b00','01-10','0 接触器放开1 接触器吸上',''),('6d00','10-00','0 接触器放开1 接触器吸上',''),('7000','10-11','0 接触器放开1 接触器吸上',''),('7100','11-00','0 接触器放开1 接触器吸上',''),('7200','11-01','0 接触器放开1 接触器吸上',''),('7300','11-10','0 接触器放开1 接触器吸上',''),('7400','11-11','0 接触器放开1 接触器吸上',''),('7500','触发信号传感器 KT 缺失','适用于 7500 到 7800：检查个别传感器和MQ/MQ1，如有需要重新插入。用诊断器 0500 功能检查','2'),('7600','触发信号传感器 TK 缺失','检查个别传感器和MQ/MQ1，如有需要重新插入。用诊断器 0500 功能检查',''),('7700','触发信号传感器 HK 缺失','检查个别传感器和MQ/MQ1，如有需要重新插入。用诊断器 0500 功能检查',''),('7800','触发信号传感器 EK 缺失','检查个别传感器和MQ/MQ1，如有需要重新插入。用诊断器 0500 功能检查',''),('7900','温度感测缺失','检查温度传感器，如必要 MZ 卡重插',''),('7A00','控制器监视缺失','检查监视传感器，如必要 MZ 卡重插',''),('7C00','虽然运转命令存在但 CPI 控制器断线','仅发生于含外部参数设定的 CPI（检查控制器内部的监视功能）','N5'),('7E01','MH3：写入 EEPROM 期间错误','',''),('7E02','MH3：联机设定期间 modem 无法辨识','',''),('7E03','MH3：重新搜寻 modem','',''),('7E04','MH3：从动的到主动的联机切断','',''),('7E05','MH3：写入 EEPROM 期间错误','',''),('7E06','MH3：写入 EEPROM 期间错误','',''),('7E07','MH3：写入 EEPROM 期间错误','',''),('7E08','MH3：DOS 下载请求','',''),('7E09','MH3：最初状态重置','',''),('7E0A','MH3：写入 EEPROM 期间错误','',''),('7EA4','MC3：从 MH3 重置','','N1'),('7EA5','MC3：来自 MH3 两个交握程序错误','',''),('7EA6','MC3：到 MH3 周期性传输缺失','','N1'),('7EA7','MC3：储存状态后重置','自 MH3 完成需求','N1'),('7Exx','MH3：xx＝00…7F，来自 MH3 内部的错误MC3：xx＝80…FF，MC3 辨识 MH3 错误','',''),('7F8E','MCx 触发 MM 或 ME 的起始','',''),('7F8F','起因于 MM 或 ME 的重置','','N1'),('7F8d','来自 MM 或 ME 的交握传输','',''),('7Fxx','MM/ME：XX＝00…7F 是 MM 或 ME 内部的错误','MCx：XX＝80…FF 是 MCx（＝MC1，MC2 或 MC3）辨识 MM 或 ME 的错误','Xxx'),('7b00','DC24V 电压供应缺失','检查电压（MQ 卡电压亦检查）','MBS'),('7d00','CPI：无错误','',''),('7d01','CPI：控制电压 ON','',''),('7d02','CPI：监视器错误','',''),('7d03','CPI：SMR（状态监视程序）缺失','',''),('7d04','CPI：SMR 到 TCM 控制','',''),('7d05','CPI：EEPROM 错误','',''),('7d06','CPI：散热器过热','',''),('7d07','CPI：驱动马达过热','',''),('7d08','CPI：接地缺陷讯息','',''),('7d09','CPI：主电源未确认','',''),('7d0A','CPI：直流环节电压过低','查询整个参数-输入面板',''),('7d0C','CPI：直流环节电压过高','',''),('7d0E','CPI：过电流','',''),('7d0F','CPI：主电压过高','',''),('7d0b','CPI：有效电力的允许脉动','',''),('7d0d','CPI：错误堆栈删除','',''),('7d10','CPI：DSP 时间错误','DSP＝CPI 内数字信号处理器',''),('7d11','CPI：±15V 或 24V 过低','',''),('7d12','CPI：No.18 错误（一般未使用）','',''),('7d13','CPI：CAN 扁平电缆错误','',''),('7d14','CPI：电压实际值≠参考值±10﹪','',''),('7d15','CPI：DSP 电流控制器错误','',''),('7d16','CPI：DSP 重置','',''),('7d17','CPI：到 DSP 的不明讯号','',''),('7d18','CPI：传输参考值编号错误','',''),('7d19','CPI：运转接触器有问题','',''),('7d1A','CPI：档板设定','',''),('7d1C','CPI：脉冲发电机缺失','',''),('7d1E','CPI：煞车错误','',''),('7d1F','CPI：马达或煞车过热','',''),('7d1b','CPI：脉冲发电机刻度范围错误','',''),('7d1d','CPI：成功的脉冲发电机刻度','',''),('7d20','CPI：sin-cos 发电机错误','',''),('7d21','CPI：回授放大组件未准备好','',''),('7d84','MC3：CPI 控制器重置','','N1'),('7d85','MC3：来自 CPI 的两个交握讯号流失','交握是定义如两电路板间周期性数据转换',''),('7d86','MC3：到 CPI 周期性传输的缺失','','N1'),('7dxx','CPI：事件 xx','',''),('8000','错误的车厢命令','当电梯位于最低楼仍命令下行','N1'),('8100','错误的车厢命令','当电梯位于最高楼仍命令上行','N1'),('8200','不明的车厢位置','注：重新 Tech-in，如失败检查 CPU 的 5V电压或更换 CPU 上的 EEPROM','N3'),('8300','不明的车厢位置','注：重新 Tech-in，如失败检查 CPU 的 5V电压或更换 CPU 上的 EEPROM',''),('8400','不明的车厢位置','注：重新 Tech-in，如失败检查 CPU 的 5V电压或更换 CPU 上的 EEPROM',''),('8500','不明的车厢位置','注：重新 Tech-in，如失败检查 CPU 的 5V电压或更换 CPU 上的 EEPROM',''),('8600','煞车检出电路失误（自 TCI 工作程序版本 06.95/25 以后）','检查煞车检出传感器的设置。监视器可经由tech-in 的 AF0d 功能取消。','MNS'),('8601','整个安全回路接通期间，煞车被中断开','有缺陷',''),('8701','额定速度 VN','说明：8701-870c减速斜率等内存位置未被写入程序或写入不恰当。在这个部分，电梯特殊程序必须被制成现成的，在改编程序形式中命令程序部门，指定错误码编码。特殊程序内存位置可使用诊断器单元 I 查询也可参考功能 0000 内存位置',''),('8702','最大速度 VCON','说明：8701-870c减速斜率等内存位置未被写入程序或写入不恰当。在这个部分，电梯特殊程序必须被制成现成的，在改编程序形式中命令程序部门，指定错误码编码。特殊程序内存位置可使用诊断器单元 I 查询也可参考功能 0000 内存位置',''),('8703','加速斜率 ａ','说明：8701-870c减速斜率等内存位置未被写入程序或写入不恰当。在这个部分，电梯特殊程序必须被制成现成的，在改编程序形式中命令程序部门，指定错误码编码。特殊程序内存位置可使用诊断器单元 I 查询也可参考功能 0000 内存位置',''),('8704','减速斜率 －ａ','说明：8701-870c减速斜率等内存位置未被写入程序或写入不恰当。在这个部分，电梯特殊程序必须被制成现成的，在改编程序形式中命令程序部门，指定错误码编码。特殊程序内存位置可使用诊断器单元 I 查询也可参考功能 0000 内存位置',''),('8705','急拉','说明：8701-870c减速斜率等内存位置未被写入程序或写入不恰当。在这个部分，电梯特殊程序必须被制成现成的，在改编程序形式中命令程序部门，指定错误码编码。特殊程序内存位置可使用诊断器单元 I 查询也可参考功能 0000 内存位置',''),('8706','急拉 1','说明：8701-870c减速斜率等内存位置未被写入程序或写入不恰当。在这个部分，电梯特殊程序必须被制成现成的，在改编程序形式中命令程序部门，指定错误码编码。特殊程序内存位置可使用诊断器单元 I 查询也可参考功能 0000 内存位置',''),('8707','急拉 2','说明：8701-870c减速斜率等内存位置未被写入程序或写入不恰当。在这个部分，电梯特殊程序必须被制成现成的，在改编程序形式中命令程序部门，指定错误码编码。特殊程序内存位置可使用诊断器单元 I 查询也可参考功能 0000 内存位置',''),('8708','急拉 3','说明：8701-870c减速斜率等内存位置未被写入程序或写入不恰当。在这个部分，电梯特殊程序必须被制成现成的，在改编程序形式中命令程序部门，指定错误码编码。特殊程序内存位置可使用诊断器单元 I 查询也可参考功能 0000 内存位置',''),('8709','急拉 4','说明：8701-870c减速斜率等内存位置未被写入程序或写入不恰当。在这个部分，电梯特殊程序必须被制成现成的，在改编程序形式中命令程序部门，指定错误码编码。特殊程序内存位置可使用诊断器单元 I 查询也可参考功能 0000 内存位置',''),('870A','调整运转速度 VJ','说明：8701-870c减速斜率等内存位置未被写入程序或写入不恰当。在这个部分，电梯特殊程序必须被制成现成的，在改编程序形式中命令程序部门，指定错误码编码。特殊程序内存位置可使用诊断器单元 I 查询也可参考功能 0000 内存位置',''),('870C','保养速度 VJ','说明：8701-870c减速斜率等内存位置未被写入程序或写入不恰当。在这个部分，电梯特殊程序必须被制成现成的，在改编程序形式中命令程序部门，指定错误码编码。特殊程序内存位置可使用诊断器单元 I 查询也可参考功能 0000 内存位置',''),('870b','重新调整运转速度 VN','说明：8701-870c减速斜率等内存位置未被写入程序或写入不恰当。在这个部分，电梯特殊程序必须被制成现成的，在改编程序形式中命令程序部门，指定错误码编码。特殊程序内存位置可使用诊断器单元 I 查询也可参考功能 0000 内存位置',''),('87PP','特殊程序中必要的 MW1 参数值缺乏。个别的错误参数能被限定于基本变量 PP 上（如 8704＝减速斜率；瞬时值未允许）','',''),('8800','煞车盘动作未达标准','实际动作监视电路的响应',''),('89…','错误的操作码1、Byte：片段码高2、Byte：片段码低3、指令指示器高4、指令指示器低','伴随 56xx 后发生且连续储存 4 次。读取整段错误码包含潜码 xx，联络 VTS 或 QMS 部门','SM1'),('8A01','加速斜率','',''),('8A02','减速斜率','',''),('8A03','煞车作用时间','',''),('8A04','急拉（整体的）','',''),('8A05','1、急拉','',''),('8A06','2、急拉','',''),('8A07','3、急拉','',''),('8A08','4、急拉','',''),('8A09','加速斜率预先控制','',''),('8A0A','增益','',''),('8A0C','保养驾驶速度','',''),('8A0E','重拉水平速度','',''),('8A0F','上行强迫减速点','',''),('8A0b','额定速度','',''),('8A0d','调整运转速度','',''),('8A10','下行强迫减速点','',''),('8A11','着床速度','',''),('8A12','着床距离','',''),('8A…','参数设定超出 MW1 卡容许范围 错误仅发生于起始期间','',''),('9000','安全回路接通时速度＞0.5m/s','安全回路经 SR 模块接通且 CPU 检测速度＞0.5m/s。可能当错误的预先准备运转，在停滞时回授脉冲发电机仍有脉冲讯号','N2'),('9100','安全回路接通时车厢未在门区域位置','安全回路经 SR 模块接通且 CPU 未侦测到楼码片。可能原因：油压梯的上下变动；如果车厢停止在非门区域（如钢索打滑）或极限框架内','N2'),('9200','在停车或停滞状态时 V＞0.3m/s','脉冲发电机，特别形号 Wachendorf，在停滞状态仍有脉冲输出。更换 11.95 以后改良的脉冲发电机。自 TCI 工作版本 06.95 以后于停滞时速度不大于监视状态。','N6'),('9300','重拉水平速度＞0.2m/s ','在停车或停滞状态时重拉水平速度＞0.2m/s','N6'),('9400','速度监视装置跳脱','监视器反应在 V+10％；特殊工作作用也可能（10％限速器开关的替代）','SM1'),('9500','驱动监视装置的反应（16M，25M，API/CPI，使用 Beringer 可变速油压梯）','温度监视欠逆向监视参考/实际值监视（beringer）驱动控制器停止等API/CPI 参考参数输入器错误码','MN2'),('9900','MW1 速度监视','操作状态 00，01 或 04 速度＞0.3m/s 的错误','N1'),('9A00','安全回路经 SR 模块接通时 V＞0.5m/s 输入MW1','操作状态 03 速度＞0.5m/s 的错误 N19b00 保养驾驶速度监视 操作状态 07 速度＞0.63m/s（EN81）速度＞0.4m/s（Russia）的错误','N1'),('9E00','减速斜率监视第三轨，光栅装置','检查光栅','MS1'),('9F00','减速斜率监视第三轨，减速斜率监视跳脱','含缓冲器的高速电梯缓冲器降低','N1'),('C000|d000','接近停楼时加/减速斜率太陡','MD/MD1 加/减速斜率调整较平缓后 Techin','N1'),('C100|d100','改变装置反应','减速点太接近楼码确认勾。加/减速斜率调整较平缓后 Techin','N1'),('C200|d200','改变装置反应','加速顶点超出加速斜率范围。加/减速斜率调整较平缓后 Techin','N1'),('C300|d300','改变装置反应','参考/实际值偏差过大（电梯过快）加/减速斜率调整较平缓后 Techin','N1'),('C400|d400','改变装置反应','同 C300/d300','N1'),('C500|d500','MD/MD1－CPU 信号转换错误','加速顶点，减速点或停止点过头。脉冲发电机异常或打滑；调整加速斜率后 Tech-in','N1'),('C600|d600','MD/MD1－CPU 信号转换错误','车厢在两个门区域间。假设点在门最后离开的区域内。同 C500/d500','N1'),('C700|d700','MD/MD1－CPU 信号转换错误','路径实际值已校正。同 C500/d500','N1'),('C800|d800','如果 AF13＆AF20 在 Tech-in 模式中未写入，超过值的范围','执行 tech-in',''),('C900|D900','无运转操控','','N'),('CA00|dA00','无运转操控','','N'),('CAN事件来自 MC1/MC2/MC3界面（CANL＝车厢扁平电缆）','','',''),('CAN事件来自 MC3界面（C ANS＝坑道扁平电缆）','','',''),('CAN事件来自 MF3或 MF3D','','',''),('CAN事件来自 MZ1 关于坑道/车厢','','',''),('CAN事件来自 MZ1 关于车厢扁平电缆','','',''),('CAN－ MP 卡错误（0MP 上到 15MP）','','',''),('CC00|dC00','无运转操控','','N'),('CE00|dE00','无运转操控','','N'),('CPI 控制器内事件','','',''),('CPU-MW/MW1 联络','','',''),('Cb00|db00','无运转操控','','N'),('Cd00|dd00','无运转操控','','N'),('E000|E100','读取错误','CPU 的 EEPROM 有缺陷；重插 EEPROM；检查 5V 电压','SM1'),('E200','原先的 BBC 和备份检查不正确','重插 EEPROM；重新 tech-in','SM1'),('E300','原先的 BBC 和备份检查正确但不同','重插 EEPROM；重新 tech-in','SM1'),('E400','记忆装置错误','CPU 的 RAM 异常',''),('E500','备份 BBC 错误','',''),('E600','原本 BBC 错误','',''),('E700','RAM 错误','','N1'),('E800','最上停层','两停楼电梯的保养平台展开','S1'),('E801','最上停层为 0','重作 AF10；停层数（包含假停层）必须储存于特别程序内','S1'),('E900','溢出错误 AF71（强迫减速）或','AF74（超速保护）的计算导致内存位置溢出','S1'),('EAxx','MC3：不明错误 xx 到外围装置','',''),('EEyy|EExx','EEPROM 内存储器位置 xxyy 异常','更新 EEPROM',''),('F000','CPU 与 MZ1 的传输错误','0C01，C02，C03，C10，C11，0C12 导致跳脱','MS1'),('F100','MZ1 与车厢板 MF3/MF4 等的传输错误','0C04，C09，0C0A，0C0b，0C0C 导致跳脱','MS1'),('F200','MZ1 与车厢附属装置如 LSM1，F2 等的传输错误','0C0d，0C0E 导致跳脱','MS1'),('F300','MZ1 与机房扁平电缆如 MP 卡等传输错误','0C05，0C06，0C07，0C08 导致跳脱','MS1'),('F400','0C…错误引起的停止','F000 到 F300 未包含','MS1'),('F800','8kRAM/EEPROM 未侦测到','较早的错误 0203 或 0204','MS1'),('FE00','MC1：快闪数据错误（BBC 检查总和）','Tech-in 数据流失；重新 tech-in','MS1'),('Fb00','远程电话服务码','远程电话服务装置一般讯息（未包含在TCI/TCM 错误表内）',''),('Fd00','MC1：快闪数据错误（BBC 检查总和）','Tech-in 数据在 RAM 复制范围内',''),('Fd01','MC1：RAM 复制数据错误','Tech-in 资料愉闪存内 OK',''),('Fd0F','快闪数据错误','于特殊程序数据范围内的错误',''),('FdFA','特殊命令 EPROM 未作用','电梯特殊程序未被加载',''),('MC 的处理器缺失（CPU E60）','','',''),('MC1/MC2 的处理器缺失（CPU）','','',''),('MC1/MC2/MC3','','',''),('MD/MD1 与 CPU 间正确顺序检查码运转方向：C?00＝下行方向／d？00＝上行方向','','',''),('MH3 事件','','',''),('MM－ME 事件','','',''),('MQ 卡','','',''),('MQ1 事件','','',''),('MZ/MZ1','','',''),('MZ1/CPU','','',''),('TCI/TCM 一般性错误','','',''),('TCI/TCM 控制盘错误','','',''),('TCI/TCM 错误','','',''),('TCM 控制-MD1 卡运转方向：C?00＝下行方向／d？00＝上行方向','','',''),('TCM 控制系统的错误','','',''),('TCM－API 的 FIS 接口（在 API 控制器内）','','',''),('b000','操作状态错误','选择器无法辨识正确的操作状态','N3'),('一般性错误','','',''),('主门驱动','','',''),('使用 CPU（E60）的 TCM（CAN）运行控制的错误','','',''),('使用 MC1 卡 CPU 的错误','','',''),('使用 MC1 错误码 2C00 到 2F00 包含子码位置 XX','','',''),('使用目标选择控制（DCS）TCM的错误','','',''),('副门驱动','','',''),('参考-实际值监视','','',''),('安全回路','','',''),('无机房电梯','','',''),('自 12.08.96 版本以后 TCI/TCM 新增错误码','','',''),('错误码','错误说明','原因及修理指南','备注')"
    cur.execute(sql)
    conn.commit()
    sql=f"INSERT INTO `hitachi_mca` VALUES ('10','电路标准电压异','电路标准电压异常'),('11','  #50B ON 故障',''),('12','  #5    ON 故障','副微机停机'),('13','安全回路动作故','综合微机与副微机通信'),('14','软件WDT 动作检','双重输入缓冲器故障'),('15','      VR1 P48V 电源','  INV 输出封锁电路 OFF'),('16','检修运行输入信',''),('17','号机 NO.异常',''),('18','连续 3 次开门锁','  #50B    ON 故障'),('19','   ，ORS 经',''),('1A','  40D OFF 故障','＃ 15B    ON 故障'),('42','  40G ON 故障','      50B       OFF 故障'),('43','  40D ON 故障','   SDS1 同时 ON 故障'),('44','  #5    OFF 故障','   15B    OFF  故障'),('45','  #5R OFF 故障','滑轮滑动检测'),('46','运行指令输入缓',''),('48','连续 3 次开门不成功','电流不足检出'),('62','门机电源切断无效故','速度偏差异常'),('80','   FMLX 、FMLY 、#100RXA 、B OFF 故',''),('81','  门机电源 OFF 故障',''),('82','  开关门堵死故障',''),('83','   FMLX 、ON 故障检出',''),('84','   FMLY    ON 故障检出',''),('90','    SCLB3 板通信故障','负荷检测电路异常'),('92','  综合微机重启多次所导致的最近楼层',''),('93','  散热片过热保护动作','  SDS 不动作(SDS ON 故'),('96','   ROM 和数错误 1','过电压发生次数 10 次'),('97','   ROM 和数错误','现场调整区规格表和数'),('9D','  旋转编码器断线，逆相故障','  CNV 侧 霍尔 CT 故障'),('A0','逆转检出','DZA 位置检测器 OPEN'),('A1','  旋转编码器磁极位置异常','DZB 位置检测器 OPEN'),('A6','   ALP 异常',''),('A7','   #5R OFF 故障','多次自救检出'),('A9','   #40D 接触器故障','  SDS 强制减速开关多次'),('AE','  开门锁死导致运行至其他层 (1 回)',''),('AF','  光幕异常',''),('B0','变频门机故障',''),('B1','变频门机微机死机故障',''),('C0','群管理-号机通信故障',''),('C2','待机系微机异常',''),('C3','运行系微机异常',''),('C4','共通厅外召唤回路异常',''),('C5','群管理微机死机',''),('C6','单梯厅外召唤回路异常',''),('C9','   FMLX OFF 故障检出',''),('CA','   FMLY OFF 故障检出',''),('CB','   #100RXA 、B OFF 故障检出',''),('D1','   CLS 、OLS 同时 ON 故障','转矩测定运行异常'),('D7','曾经发生开门或关门锁死故','过电压发生次数 5 次以上'),('D8','开门时 ORS 连续动作故障',''),('D9','关门时 ORS 连续动作故障',''),('E3','   SCLB3 板通信故障(预报)',''),('EF','工程用层高测定规格表 ON','   SDS  速度异常 1')"
    cur.execute(sql)
    conn.commit()
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
#    Application()
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
            data = {
                "host": "111.173.83.23",
                "user": "root",
                "password": "Wqq@123456",
                "db": "test",
                "charset": "utf8"
            }
            if not os.path.exists("auto.json"):
                json_str = json.dumps(data, indent=4)
                with open("auto.json", "w") as f:
                    f.write(json_str)
            else:
                file = open('auto.json', 'rb')
                jsonData = json.load(file)
                host = jsonData['host']
                user = jsonData['user']
                pwd = jsonData['password']
                db = jsonData['db']
                charset = jsonData['charset']
                conn = pymysql.connect(host=host, user=user, password=pwd, db=db, charset=charset)
                cur = conn.cursor()

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
# -------------娱乐相关-----------------
@app.route('/chess')
def chinese_chess():
    return render_template("chess.html")

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
    data = {
        "host": "111.173.83.23",
        "user": "root",
        "password": "Wqq@123456",
        "db": "test",
        "charset": "utf8"
    }
    if not os.path.exists("auto.json"):
        json_str = json.dumps(data, indent=4)
        with open("auto.json", "w") as f:
            f.write(json_str)
    else:
        file = open('auto.json', 'rb')
        jsonData = json.load(file)
        host = jsonData['host']
        user = jsonData['user']
        pwd = jsonData['password']
        db = jsonData['db']
        charset = jsonData['charset']
        conn = pymysql.connect(host=host, user=user, password=pwd, db=db, charset=charset)
        cur = conn.cursor()

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
        data = {
            "host": "111.173.83.23",
            "user": "root",
            "password": "Wqq@123456",
            "db": "test",
            "charset": "utf8"
        }
        if not os.path.exists("auto.json"):
            json_str = json.dumps(data, indent=4)
            with open("auto.json", "w") as f:
                f.write(json_str)
        else:
            file = open('auto.json', 'rb')
            jsonData = json.load(file)
            host = jsonData['host']
            user = jsonData['user']
            pwd = jsonData['password']
            db = jsonData['db']
            charset = jsonData['charset']
            conn = pymysql.connect(host=host, user=user, password=pwd, db=db, charset=charset)
            cur = conn.cursor()
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
        data = {
            "host": "111.173.83.23",
            "user": "root",
            "password": "Wqq@123456",
            "db": "test",
            "charset": "utf8"
        }
        if not os.path.exists("auto.json"):
            json_str = json.dumps(data, indent=4)
            with open("auto.json", "w") as f:
                f.write(json_str)
        else:
            file = open('auto.json', 'rb')
            jsonData = json.load(file)
            host = jsonData['host']
            user = jsonData['user']
            pwd = jsonData['password']
            db = jsonData['db']
            charset = jsonData['charset']
            conn = pymysql.connect(host=host, user=user, password=pwd, db=db, charset=charset)
            cur = conn.cursor()
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
            createdb()
        return 'Error:{}——{}'.format(e, ee), '程序出错'
    except TimeoutError as err:
        return 'Error:{}'.format(err), '程序超时'


def getconn_data():
    try:
        data = {
            "host": "111.173.83.23",
            "user": "root",
            "password": "Wqq@123456",
            "db": "test",
            "charset": "utf8"
        }
        if not os.path.exists("auto.json"):
            json_str = json.dumps(data, indent=4)
            with open("auto.json", "w") as f:
                f.write(json_str)
        else:
            file = open('auto.json', 'rb')
            jsonData = json.load(file)
            host = jsonData['host']
            user = jsonData['user']
            pwd = jsonData['password']
            db = jsonData['db']
            charset = jsonData['charset']
            conn = pymysql.connect(host=host, user=user, password=pwd, db=db, charset=charset)
            cur = conn.cursor()
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
        data = {
            "host": "111.173.83.23",
            "user": "root",
            "password": "Wqq@123456",
            "db": "test",
            "charset": "utf8"
        }
        if not os.path.exists("auto.json"):
            json_str = json.dumps(data, indent=4)
            with open("auto.json", "w") as f:
                f.write(json_str)
        else:
            file = open('auto.json', 'rb')
            jsonData = json.load(file)
            host = jsonData['host']
            user = jsonData['user']
            pwd = jsonData['password']
            db = jsonData['db']
            charset = jsonData['charset']
            conn = pymysql.connect(host=host, user=user, password=pwd, db=db, charset=charset)
            cur = conn.cursor()
            sql = "create database test"
            cur.execute(sql)
            cur.close()
            conn.close()
    except Exception as ee:
        if '1049' in ee:
            createdb()
        data = None
        return data
def setting():
    data = {
        "host": "111.173.83.23",
        "user": "root",
        "password": "Wqq@123456",
        "db": "test",
        "charset": "utf8"
    }
    if not os.path.exists("auto.json"):
        json_str = json.dumps(data, indent=4)
        with open("auto.json", "w") as f:
            f.write(json_str)

if __name__ == '__main__':
    # 端口号设置
    setting()
    app.run(host="0.0.0.0", port=5672,debug=True)
