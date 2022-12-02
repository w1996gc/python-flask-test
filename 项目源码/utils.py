import json
import os
import time
import pymysql


def get_time():
    time_str = time.strftime("%Y{}%m{}%d{} %X")
    return time_str.format("年", "月", "日")



def get_conn():
    # 建立连接
    data = {
        "host": "111.173.83.23",
        "user": "root",
        "password": "123456",
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
        conn = pymysql.connect(host=host, user=user, password=pwd, db=db, charset=charset)  # c创建游标A
        cursor = conn.cursor()
        return conn, cursor


def query_no(sql):
    """

    :param sql:
    :return:
    """
    conn, cursor = get_conn()
    cursor.execute(sql)
    res = cursor.fetchall()
    conn.commit()
    close_conn(conn, cursor)
    return res


def close_conn(conn, cursor):
    if cursor:
        cursor.close()
    if conn:
        conn.close()


def query(sql, *args):
    """

    :param sql:
    :param args:
    :return:
    """
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    conn.commit()
    close_conn(conn, cursor)
    return res

def create_date():
    data = {
        "host": "111.173.83.23",
        "user": "root",
        "password": "123456",
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

    # sql4 = f"create database `test`"
    # cur.execute(sql4)
    # cur.close()
    # conn.close()
    # sql5 = f"CREATE TABLE `test`.`sys_user`  (`id` int NOT NULL AUTO_INCREMENT,`username` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,`password` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,`name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,`email` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,`phone` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,PRIMARY KEY (`id`) USING BTREE) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;"
    # cur.execute(sql5)
    # cur.close()
    # conn.close()

        sql1=f"CREATE TABLE `test`.`details`  (`id` int NOT NULL AUTO_INCREMENT,`update_time` datetime NULL DEFAULT NULL COMMENT '数据最后更新时间',`province` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '省',`city` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '市',`confirm` int NULL DEFAULT NULL COMMENT '累计确诊',`confirm_add` int NULL DEFAULT NULL COMMENT '新增治愈',`heal` int NULL DEFAULT NULL COMMENT '累计治愈',`dead` int NULL DEFAULT NULL COMMENT '累计死亡',PRIMARY KEY (`id`) USING BTREE) ENGINE = InnoDB AUTO_INCREMENT = 552 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;"
        cur.execute(sql1)
        cur.close()
        conn.close()
        sql2=f"CREATE TABLE `test`.`history`  (`ds` datetime NOT NULL COMMENT '日期',`confirm` int NULL DEFAULT NULL COMMENT '累计确诊',`confirm_add` int NULL DEFAULT NULL COMMENT '当日新增确诊',`suspect` int NULL DEFAULT NULL COMMENT '剩余疑似',`suspect_add` int NULL DEFAULT NULL COMMENT '当日新增疑似',`heal` int NULL DEFAULT NULL COMMENT '累计治愈',`heal_add` int NULL DEFAULT NULL COMMENT '当日新增治愈',`dead` int NULL DEFAULT NULL COMMENT '累计死亡',`dead_add` int NULL DEFAULT NULL COMMENT '当日新增死亡',PRIMARY KEY (`ds`) USING BTREE) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;"
        cur.execute(sql2)
        cur.close()
        conn.close()
        sql3=f"CREATE TABLE `test`.`hotsearch`  (`id` int NOT NULL AUTO_INCREMENT,`dt` datetime NULL DEFAULT NULL,`content` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,PRIMARY KEY (`id`) USING BTREE) ENGINE = InnoDB AUTO_INCREMENT = 61 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = DYNAMIC;"
        cur.execute(sql3)
        cur.close()
        conn.close()

def test():
    sql = "select * from details"
    res = query(sql)
    return res[0]


def get_c1_data():
    sql = "select sum(confirm)," \
          "(select suspect from history order by ds desc limit 1)," \
          "sum(heal),sum(dead) from details " \
          "where update_time=(select update_time from details order by update_time desc limit 1) "
    res = query(sql)
    return res[0]


def get_c2_data():
    sql = "select province,sum(confirm) from details " \
          "where update_time=(select update_time from details " \
          "order by update_time desc limit 1) " \
          "group by province"
    res = query(sql)
    return res


def get_l1_data():
    sql = "select ds,confirm,suspect,heal,dead from history"
    res = query(sql)
    return res


def get_l2_data():
    sql = "select ds,confirm_add,suspect_add from history"
    res = query(sql)
    return res


def get_r1_data():
    sql = 'select city,confirm from (select city,confirm from details where city not in ("地区待确认","境外输入") and DATE_FORMAT(update_time, "%Y-%m-%d")=(select DATE_FORMAT(update_time, "%Y-%m-%d") from details order by update_time desc limit 1) and province not in ("北京","上海","天津","重庆","香港") union all select province as city,sum(confirm) as confirm from details where DATE_FORMAT(update_time, "%Y-%m-%d") =(select DATE_FORMAT(update_time, "%Y-%m-%d") from details order by update_time desc limit 1) and province in ("北京","上海","天津","重庆","香港") group by province) as a order by confirm desc limit 10'
    res = query_no(sql)
    return res


def get_r2_data():
    sql = "select content from hotsearch order by id desc limit 20"
    res = query(sql)
    return res


def get_user(username, password):
    sql = "select id from sys_user where username= '" + username + "' and password= '" + password + "'"
    res = query(sql)
    return res


def get_old_list(page_size, page_no, param):
    count_sql = "select count(*) from history where " + param
    count_res = query(count_sql)[0][0]
    start = page_size * (page_no - 1)
    start = 0 if start < 0 else start
    sql = "select * from history where " + param + " order by ds desc limit " + str(start) + "," + str(page_size)
    res = query(sql)
    data_page = []
    page_list = []
    max_page = 0
    if count_res % page_size == 0:
        max_page = int(count_res / page_size)
    else:
        max_page = int(count_res / page_size) + 1
    if max_page <= 5:
        page_list = [i for i in range(1, max_page + 1, 1)]
    elif page_no + 2 > max_page:
        page_list = [i for i in range(max_page - 5, max_page + 1, 1)]
    elif page_no - 2 < 1:
        page_list = [i for i in range(1, 6, 1)]
    else:
        page_list = [i for i in range(page_no - 2, page_no + 3, 1)]
    for a, b, c, d, e, f, g, h, i in res:
        item = [a.strftime("%Y-%m-%d"), b, c, d, e, f, g, h, i]
        data_page.append(item)
    return data_page, count_res, page_list, max_page


def get_new_list(page_size, page_no, param):
    param = param.replace("\\", "")
    count_sql = "select count(*) from details where " + param
    count_res = query_no(count_sql)[0][0]
    start = page_size * (page_no - 1)
    start = 0 if start < 0 else start
    sql = "select * from details where " + param + " order by id desc limit " + str(start) + "," + str(page_size)
    res = query(sql)
    data_page = []
    page_list = []
    max_page = 0
    if count_res % page_size == 0:
        max_page = int(count_res / page_size)
    else:
        max_page = int(count_res / page_size) + 1
    if max_page <= 5:
        page_list = [i for i in range(1, max_page + 1, 1)]
    elif page_no + 2 > max_page:
        page_list = [i for i in range(max_page - 5, max_page + 1, 1)]
    elif page_no - 2 < 1:
        page_list = [i for i in range(1, 6, 1)]
    else:
        page_list = [i for i in range(page_no - 2, page_no + 3, 1)]
    for a, b, c, d, e, f, g, h in res:
        item = [a, b.strftime("%Y-%m-%d"), c, d, e, f, g, h]
        data_page.append(item)
    return data_page, count_res, page_list, max_page


def get_news_list(page_size, page_no, param):
    param = param.replace("\\", "")
    count_sql = "select count(*) from hotsearch where " + param
    count_res = query(count_sql)[0][0]
    start = page_size * (page_no - 1)
    start = 0 if start < 0 else start
    sql = "select * from hotsearch where " + param + " order by id desc limit " + str(start) + "," + str(page_size)
    res = query(sql)
    data_page = []
    if count_res % page_size == 0:
        max_page = int(count_res / page_size)
    else:
        max_page = int(count_res / page_size) + 1
    if max_page <= 5:
        page_list = [i for i in range(1, max_page + 1, 1)]
    elif page_no + 2 > max_page:
        page_list = [i for i in range(max_page - 5, max_page + 1, 1)]
    elif page_no - 2 < 1:
        page_list = [i for i in range(1, 6, 1)]
    else:
        page_list = [i for i in range(page_no - 2, page_no + 3, 1)]
    for a, b, c in res:
        item = [a, b.strftime("%Y-%m-%d %H:%M:%S"), c]
        data_page.append(item)
    return data_page, count_res, page_list, max_page


def edit_old(ds, confirm, confirm_add, suspect, suspect_add, heal, heal_add, dead, dead_add):
    sql = "update history set confirm=" + confirm + ",confirm_add=" + confirm_add + ",suspect=" + suspect + ",suspect_add=" + suspect_add + ",heal=" + heal + ",heal_add=" + heal_add + ",dead=" + dead + ",dead_add=" + dead_add + " where ds ='" + ds + "'"
    res = query(sql)
    return res


def edit_new(id, confirm, confirm_add, heal, dead):
    sql = "update details set confirm=" + confirm + ",confirm_add=" + confirm_add + ",heal=" + heal + ",dead=" + dead + " where id =" + id
    res = query(sql)
    return res


def edit_news(id, content):
    sql = "update hotsearch set content='" + content + "' where id =" + id
    res = query(sql)
    return res


def del_old(ds):
    sql = "delete from history where ds ='" + ds + "'"
    res = query(sql)
    return res


def del_new(id):
    sql = "delete from  details where id =" + id
    res = query(sql)
    return res


def del_news(id):
    sql = "delete from  hotsearch where id =" + id
    res = query(sql)
    return res

def get_register(n,user,password,mail,photonumber):
    # 建立数据库连接
    try:
        data = {
            "host": "111.173.83.23",
            "user": "root",
            "password": "123456",
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
            cur=conn.cursor()
            sql=f"INSERT INTO `sys_user` VALUES (%s, '%s', '%s', '管理员', '%s', '%s')"%(n,user,password,mail,photonumber)
            print(sql)
            cur.execute(sql)
            conn.commit()
            cur.close()
            conn.close()
            return '200'
    except Exception as ee:
        if '1049' in ee:
            create()
        return '200'

def get_data_clear():
    data = {
        "host": "111.173.83.23",
        "user": "root",
        "password": "123456",
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
        cur=conn.cursor()
        sql1=f"truncate table details"
        sql2=f"truncate table hotsearch"
        sql3=f"truncate table history"
        cur.execute(sql1)
        cur.execute(sql2)
        cur.execute(sql3)
        cur.close()
        conn.close()
        return '200'

def get_user_list(page_size, page_no, param):
    # 建立数据库连接
    # conn = pymysql.connect(host="111.173.83.23", user="root", password="123456", db="test", charset="utf8")
    # cur=conn.cursor()
    count_sql="select count(*) from sys_user where " + param
    count_res = query(count_sql)[0][0]
    start = page_size * (page_no - 1)
    start = 0 if start < 0 else start
    sql = "select * from sys_user where " + param + " order by ds desc limit " + str(start) + "," + str(page_size)
    res = query(sql)
    data_page = []
    page_list = []
    max_page = 0
    if count_res % page_size == 0:
        max_page = int(count_res / page_size)
    else:
        max_page = int(count_res / page_size) + 1
    if max_page <= 5:
        page_list = [i for i in range(1, max_page + 1, 1)]
    elif page_no + 2 > max_page:
        page_list = [i for i in range(max_page - 5, max_page + 1, 1)]
    elif page_no - 2 < 1:
        page_list = [i for i in range(1, 6, 1)]
    else:
        page_list = [i for i in range(page_no - 2, page_no + 3, 1)]
    for a, b, c, d, e, f, g, h, i in res:
        item = [a.strftime("%Y-%m-%d"), b, c, d, e, f, g, h, i]
        data_page.append(item)
    return data_page, count_res, page_list, max_page

def create():
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
        try:
            sql2=f"create database `test`"
            cur.execute(sql2)
            cur.close()
            conn.close()

            sql1 = f"CREATE TABLE `test`.`sys_user`  (`id` int NOT NULL AUTO_INCREMENT,`username` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,`password` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,`name` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,`email` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,`phone` varchar(50) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL,PRIMARY KEY (`id`) USING BTREE) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8 COLLATE = utf8_general_ci ROW_FORMAT = DYNAMIC;"
            cur.execute(sql1)
            cur.close()
            conn.close()
            return True
        except Exception:
            return False
