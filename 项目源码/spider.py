import time
import datetime
from selenium.webdriver.common.by import By
import pymysql
import json
import traceback
import requests
from selenium.webdriver import Chrome,Firefox, FirefoxOptions,ChromeOptions
import pandas as pd
from bs4 import BeautifulSoup
import re


def get_conn():
    # 建立数据库连接
    conn = pymysql.connect(host="111.173.83.23", user="root", password="Wqq@123456", db="test", charset="utf8")
    # 创建游标
    cursor = conn.cursor()
    return conn, cursor


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


##################爬虫独立模块######################
# 功能说明：
#   ①爬取并插入各个地区历史疫情数据
#   ②爬取并插入全国历史疫情统计数据
#   ③爬取并插入百度新闻标题最新数据
# 文件说明：
#   ①可独立运行呈现结果
#   ②调用online方法运行
####################################################
def get_tx_history_data():
    url2 = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_other"
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36'
    }
    r2 = requests.get(url2, headers)

    res2 = json.loads(r2.text)

    try:
        data_all2 = json.loads(res2["data"])
    except:
        return [], []
    history = {}
    for i in data_all2["chinaDayList"]:
        ds = i["y"] + "." + i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")  # 匹配时间
        ds = time.strftime("%Y-%m-%d", tup)  # 改变时间格式
        confirm = i["confirm"]
        suspect = i["suspect"]
        heal = i["heal"]
        dead = i["dead"]
        history[ds] = {"confirm": confirm, "suspect": suspect, "heal": heal, "dead": dead}
    for i in data_all2["chinaDayAddList"]:
        ds = i["y"] + "." + i["date"]
        tup = time.strptime(ds, "%Y.%m.%d")  # 匹配时间
        ds = time.strftime("%Y-%m-%d", tup)  # 改变时间格式
        confirm = i["confirm"]
        suspect = i["suspect"]
        heal = i["heal"]
        dead = i["dead"]
        if ds in history:
            history[ds].update({"confirm_add": confirm, "suspect_add": suspect, "heal_add": heal, "dead_add": dead})
    return history


def get_tx_detail_data():
    url1 = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
    headers = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Mobile Safari/537.36'
    }
    r1 = requests.get(url1, headers)

    res1 = json.loads(r1.text)

    print(res1["data"])
    data_all1 = {}
    try:
        data_all1 = json.loads(res1["data"])
    except:
        return []

    details = []
    update_time = data_all1["lastUpdateTime"]
    data_country = data_all1["areaTree"]
    data_province = data_country[0]["children"]
    for pro_infos in data_province:
        province = pro_infos["name"]
        for city_infos in pro_infos["children"]:
            city = city_infos["name"]
            confirm = city_infos["total"]["confirm"]
            confirm_add = city_infos["today"]["confirm"]
            heal = city_infos["total"]["heal"]
            dead = city_infos["total"]["dead"]
            details.append([update_time, province, city, confirm, confirm_add, heal, dead])
    return details


def get_dx_detail_data():
    url = 'https://ncov.dxy.cn/ncovh5/view/pneumonia?from=timeline&isappinstalled=0'
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    # 省级正则表达式
    provinceName_re = re.compile(r'"provinceName":"(.*?)",')
    provinceShortName_re = re.compile(r'"provinceShortName":"(.*?)",')
    currentConfirmedCount_re = re.compile(r'"currentConfirmedCount":(.*?),')
    confirmedCount_re = re.compile(r'"confirmedCount":(.*?),')
    suspectedCount_re = re.compile(r'"suspectedCount":(.*?),')
    curedCount_re = re.compile(r'"curedCount":(.*?),')
    deadCount_re = re.compile(r'"deadCount":(.*?),')
    cities_re = re.compile(r'"cities":\[\{(.*?)\}\]')

    # 爬虫爬取数据
    datas = requests.get(url, headers=headers)
    datas.encoding = 'utf-8'
    soup = BeautifulSoup(datas.text, 'html.parser')
    data = soup.find_all('script', {'id': 'getAreaStat'})  # 网页检查定位
    data = str(data)
    data_str = data[54:-23]
    # print(data_str)

    # 替换字符串内容，避免重复查找
    citiess = re.sub(cities_re, '8888', data_str)
    # 查找省级数据
    provinceShortNames = re.findall(provinceShortName_re, citiess)
    currentConfirmedCounts = re.findall(currentConfirmedCount_re, citiess)
    confirmedCounts = re.findall(confirmedCount_re, citiess)
    suspectedCounts = re.findall(suspectedCount_re, citiess)
    curedCounts = re.findall(curedCount_re, citiess)
    deadCounts = re.findall(deadCount_re, citiess)
    details = []
    current_date = datetime.datetime.now().strftime('%Y-%m-%d')
    for index, name in enumerate(provinceShortNames):
        # 备用历史区域获取接口，只获取省份的累计确诊、现有确诊、累计治愈、累计死亡
        details.append([current_date, name, name, confirmedCounts[index], currentConfirmedCounts[index], curedCounts[index], deadCounts[index]])
    return details


# 插入地区疫情历史数据
# 插入全国疫情历史数据
def update_history():
    conn, cursor = get_conn()
    try:
        # li = get_tx_detail_data()  # 1代表最新数据
        li = get_dx_detail_data()  # 1代表最新数据
        if len(li) == 0:
            print(f"[WARN] {time.asctime()}  接口暂时异常，数据未获取到或解析地区历史疫数据异常...")
        else:
            sql = "insert into details(update_time,province,city,confirm,confirm_add,heal,dead) values(%s,%s,%s,%s,%s,%s,%s)"
            sql_query = 'select %s=(select update_time from details order by id desc limit 1)'

            # 对比当前最大时间戳
            cursor.execute(sql_query, li[0][0])

            if not cursor.fetchone()[0]:
                print(f"[INFO] {time.asctime()}  地区历史疫情爬虫已启动,正在获取数据....")
                for item in li:
                    print(f"[INFO] {time.asctime()} 已获取地区历史疫情数据：", item)
                    cursor.execute(sql, item)
                conn.commit()
                print(f"[INFO] {time.asctime()}  地区历史疫情爬虫已完成，更新到最新数据成功...")
            else:
                print(f"[WARN] {time.asctime()}地区历史疫情爬虫已启动,已是最新数据...")
    except:
        traceback.print_exc()
    try:
        dic = get_tx_history_data()  # 1代表最新数据
        if len(dic) == 0:
            print(f"[WARN] {time.asctime()}  接口暂时异常，数据未获取到或解析全国历史疫情数据异常...")
        print(f"[INFO] {time.asctime()}  全国历史疫情爬虫已启动，正在获取数据....")
        conn, cursor = get_conn()
        sql = "insert into history values (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        sql_query = "select confirm from history where ds=%s"
        for k, v in dic.items():
            if not cursor.execute(sql_query, k):
                print(f"[INFO] {time.asctime()} 已获取全国历史疫情：",
                      [k, v.get("confirm"), v.get("confirm_add"), v.get("suspect"),
                       v.get("suspect_add"), v.get("heal"), v.get("heal_add"),
                       v.get("dead"), v.get("dead_add")])
                cursor.execute(sql, [k, v.get("confirm"), v.get("confirm_add"), v.get("suspect"),
                                     v.get("suspect_add"), v.get("heal"), v.get("heal_add"),
                                     v.get("dead"), v.get("dead_add")])
        conn.commit()
        print(f"[INFO] {time.asctime()}  全国历史疫情爬虫已完成，更新到最新数据成功...")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


# 爬取百度热搜数据
def get_baidu_hot():
    option = ChromeOptions()
    option.add_argument("--headless")  # 隐藏游览器
    option.add_argument("--no-sandbox")
    option.add_argument("--disable-gpu")
    option.add_argument("--disable-dev-shm-usage")
    browser = Chrome(options=option)
    url = "https://voice.baidu.com/act/newpneumonia/newpneumonia/?from=osari_pc_3#tab1"
    browser.get(url)
    time.sleep(3)
    c = browser.find_elements(By.XPATH, "//*[@id='ptab-1']/div[3]/div/div[2]/a/div")
    context = [i.text for i in c]
    browser.close()
    return context


def is_number(s):
    try:  # 如果能运行float(s)语句，返回True（字符串s是浮点数）
        float(s)
        return True
    except ValueError:  # ValueError为Python的一种标准异常，表示"传入无效的参数"
        pass  # 如果引发了ValueError这种异常，不做任何事情（pass：不做任何事情，一般用做占位语句）
    try:
        import unicodedata  # 处理ASCii码的包
        unicodedata.numeric(s)  # 把一个表示数字的字符串转换为浮点数返回的函数
        return True
    except (TypeError, ValueError):
        pass
    return False


# 插入百度热搜实时数据
def update_hotsearch():
    cursor = None
    conn = None
    try:
        print(f"[INFO] {time.asctime()}  新闻资讯爬虫已启动，正在获取数据...")
        context = get_baidu_hot()
        conn, cursor = get_conn()
        sql = "insert into hotsearch(dt,content) values(%s,%s)"
        ts = time.strftime("%Y-%m-%d %X")
        for i in context:
            print(f"[INFO] {time.asctime()}  已获取历史疫情:", [ts, i])
            cursor.execute(sql, (ts, i))
        conn.commit()
        print(f"[INFO] {time.asctime()}  新闻资讯爬虫已完成，更新到最新数据成功...")
    except:
        traceback.print_exc()
    finally:
        close_conn(conn, cursor)


def online():
    update_history()
    update_hotsearch()
    return 200
def my_online():
    conn = pymysql.connect(
        host='111.173.83.23',
        user='root',
        password='Wqq@123456',
        db='test',
        charset='utf8'
    )

    cur = conn.cursor()
    try:
        today_time=datetime.datetime.now().date().strftime("%Y年%m月%d")
        today_time=today_time.replace('2022年','')
        sql1 = "select * from maintenance_plan where `left2-半年`='{}' order by `number` desc;".format(today_time)
        cur.execute(sql1)
        content = cur.fetchall()

        # 获取表头
        sql = "SHOW FIELDS FROM maintenance_plan"
        cur.execute(sql)
        labels = cur.fetchall()
        labels = [l[0] for l in labels]
        cur.close()
        conn.close()

        return labels, content, sql1
    except Exception as e:
        today_time=datetime.datetime.now().date().strftime("%Y年%m月%d")
        today_time1 = today_time.replace('2022年', '')
        sql1 = "select * from maintenance_plan order by `left1-半月` asc;"
        cur.execute(sql1)
        content = cur.fetchall()

        # 获取表头
        sql = "SHOW FIELDS FROM maintenance_plan"
        cur.execute(sql)
        labels = cur.fetchall()
        labels = [l[0] for l in labels]
        cur.close()
        conn.close()

        return labels, content, sql1

def _my_online(left):
    conn = pymysql.connect(
        host='111.173.83.23',
        user='root',
        password='Wqq@123456',
        db='test',
        charset='utf8'
    )

    cur = conn.cursor()
    try:
        today_time=datetime.datetime.now().date().strftime("%Y年%m月%d")
        today_time=today_time.replace('2022年','')
        sql1 = "select * from maintenance_plan where `{}`='{}' order by `number` desc;".format(left,today_time)
        cur.execute(sql1)
        content = cur.fetchall()

        # 获取表头
        sql = "SHOW FIELDS FROM maintenance_plan"
        cur.execute(sql)
        labels = cur.fetchall()
        labels = [l[0] for l in labels]
        cur.close()
        conn.close()

        return labels, content, sql1
    except Exception as e:
        today_time=datetime.datetime.now().date().strftime("%Y年%m月%d")
        today_time1 = today_time.replace('2022年', '')
        sql1 = "select * from maintenance_plan order by `left1-半月` asc;"
        cur.execute(sql1)
        content = cur.fetchall()

        # 获取表头
        sql = "SHOW FIELDS FROM maintenance_plan"
        cur.execute(sql)
        labels = cur.fetchall()
        labels = [l[0] for l in labels]
        cur.close()
        conn.close()

        return labels, content, sql1


if __name__ == "__main__":
    update_history()
    update_hotsearch()
    # print(get_baidu_hot())