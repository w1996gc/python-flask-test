#!/usr/bin/python
# -*- coding: utf-8 _*_
'''
 @File     : QB.py
 @Time     : 2022/6/16 20:35
 @Software : PyCharm
 @Author   : Tom
 @Version  : 
'''


"""
Created on 2021
@author: QB
"""
import tkinter as tk
from tkinter import ttk
import pandas as pd
from tkinter import messagebox
from tkinter import filedialog
from tkinter import END
import pymysql


class Med:
    def __init__(self, master):

        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            db='test',
            port=3306)

        self.var = tk.StringVar()
        self.var1 = tk.StringVar()
        self.var2 = tk.StringVar()
        self.var3 = tk.StringVar()
        self.var4 = tk.StringVar()
        self.var5 = tk.StringVar()
        self.var6 = tk.StringVar()
        self.var7 = tk.StringVar()
        self.var8 = tk.StringVar()

        self.columns = ['id', 'username','password','name','email','phone']
        self.tree = ttk.Treeview(
            master,  #
            height=15,  # 表格显示的行数
            columns=self.columns,  # 显示的列
            show='headings',  # 隐藏首列
        )
        for x in self.columns:
            self.tree.heading(x, text=x)
            self.tree.column(x, width=120)
        self.tree.grid(row=0, columnspan=8)  # columnspan=3合并单元格，横跨3列

        self.cursor = self.conn.cursor()
        try:
            self.cursor.execute("SELECT * FROM sys_user")
            results = self.cursor.fetchall()

            for row in results:
                idd = row[0]
                time = row[1]
                name = row[2]
                specification = row[3]
                nums = row[4]
                location = row[5]
                user = row[6]
                in_out = row[7]

                self.tree.insert('', END,
                                 values=[idd, time, name, specification, nums, location, user, in_out])  # 添加数据到末尾
        except Exception as e:
            print(e)
        finally:
            self.cursor.close()
            self.conn.close()

            #     cpt = 0 # Counter representing the ID of your code.
        #     for row in self.cursor:
        self.tree.bind("<ButtonRelease-1>", self.click_bf)
        #        # I suppose the first column of your table is ID
        #         self.tree.insert('', 'end', text=str(cpt), values=(row[1], row[2], row[3]))
        #         cpt += 1

        # 添加增加控件
        self.label0 = tk.Label(master, text='ID', font=('华文行楷', 12))
        self.label0.grid(row=1, column=0)
        self.entry0 = tk.Entry(master)
        self.entry0.grid(row=1, column=1)
        self.label1 = tk.Label(master, text='日期', font=('华文行楷', 12))
        self.label1.grid(row=2, column=0)
        self.entry1 = tk.Entry(master)
        self.entry1.grid(row=2, column=1)
        self.label2 = tk.Label(master, text='物品名', font=('华文行楷', 12))
        self.label2.grid(row=3, column=0)
        self.entry2 = tk.Entry(master)
        self.entry2.grid(row=3, column=1)
        self.label3 = tk.Label(master, text='规格', font=('华文行楷', 12))
        self.label3.grid(row=4, column=0)
        self.entry3 = tk.Entry(master)
        self.entry3.grid(row=4, column=1)
        self.label4 = tk.Label(master, text='数量', font=('华文行楷', 12))
        self.label4.grid(row=5, column=0)
        self.entry4 = tk.Entry(master)
        self.entry4.grid(row=5, column=1)
        self.label5 = tk.Label(master, text='存放位置', font=('华文行楷', 12))
        self.label5.grid(row=6, column=0)
        self.entry5 = tk.Entry(master)
        self.entry5.grid(row=6, column=1)
        self.label6 = tk.Label(master, text='使用人', font=('华文行楷', 12))
        self.label6.grid(row=7, column=0)
        self.entry6 = tk.Entry(master)
        self.entry6.grid(row=7, column=1)
        self.r1 = tk.Radiobutton(master, text='入库', variable=self.var, value='入库')
        self.r1.grid(row=8, column=0)
        self.r2 = tk.Radiobutton(master, text='出库', variable=self.var, value='出库')
        self.r2.grid(row=8, column=1)
        self.bu1 = tk.Button(master, text='添加', font=('方正舒体', 12), command=self.insert)
        self.bu1.grid(row=9, column=0)
        # self.sx1 = tk.Button(master,text='刷新',font=('方正舒体',12),command = self.refresh)
        # self.sx1.grid(row=9,column=1)

        # 添加查询控件

        self.label7 = tk.Label(master, text='ID', font=('华文行楷', 12))
        self.label7.grid(row=1, column=2)
        self.entry7 = tk.Entry(master)
        self.entry7.grid(row=1, column=3)
        self.label8 = tk.Label(master, text='日期', font=('华文行楷', 12))
        self.label8.grid(row=2, column=2)
        self.entry8 = tk.Entry(master)
        self.entry8.grid(row=2, column=3)
        self.label9 = tk.Label(master, text='物品名', font=('华文行楷', 12))
        self.label9.grid(row=3, column=2)
        self.entry9 = tk.Entry(master)
        self.entry9.grid(row=3, column=3)
        self.label10 = tk.Label(master, text='规格', font=('华文行楷', 12))
        self.label10.grid(row=4, column=2)
        self.entry10 = tk.Entry(master)
        self.entry10.grid(row=4, column=3)
        self.label11 = tk.Label(master, text='数量', font=('华文行楷', 12))
        self.label11.grid(row=5, column=2)
        self.entry11 = tk.Entry(master)
        self.entry11.grid(row=5, column=3)
        self.label12 = tk.Label(master, text='存放位置', font=('华文行楷', 12))
        self.label12.grid(row=6, column=2)
        self.entry12 = tk.Entry(master)
        self.entry12.grid(row=6, column=3)
        self.label13 = tk.Label(master, text='使用人', font=('华文行楷', 12))
        self.label13.grid(row=7, column=2)
        self.entry13 = tk.Entry(master)
        self.entry13.grid(row=7, column=3)
        self.r3 = tk.Label(master, text='出/入库', font=('华文行楷', 12))
        self.r3.grid(row=8, column=2)
        self.r4 = tk.Entry(master)
        self.r4.grid(row=8, column=3)
        self.bu2 = tk.Button(master, text='查询', font=('方正舒体', 12), command=self.query)
        self.bu2.grid(row=9, column=2)
        # self.sx2 = tk.Button(master,text='刷新',font=('方正舒体',12))
        # self.sx2.grid(row=9,column=3)

        # 添加修改控件
        self.label14 = tk.Label(master, text='ID', font=('华文行楷', 12))
        self.label14.grid(row=1, column=4)
        self.entry14 = tk.Entry(master, textvariable=self.var1)
        self.entry14.grid(row=1, column=5)
        self.label15 = tk.Label(master, text='日期', font=('华文行楷', 12))
        self.label15.grid(row=2, column=4)
        self.entry15 = tk.Entry(master, textvariable=self.var2)
        self.entry15.grid(row=2, column=5)
        self.label16 = tk.Label(master, text='物品名', font=('华文行楷', 12))
        self.label16.grid(row=3, column=4)
        self.entry16 = tk.Entry(master, textvariable=self.var3)
        self.entry16.grid(row=3, column=5)
        self.label17 = tk.Label(master, text='规格', font=('华文行楷', 12))
        self.label17.grid(row=4, column=4)
        self.entry17 = tk.Entry(master, textvariable=self.var4)
        self.entry17.grid(row=4, column=5)
        self.label18 = tk.Label(master, text='数量', font=('华文行楷', 12))
        self.label18.grid(row=5, column=4)
        self.entry18 = tk.Entry(master, textvariable=self.var5)
        self.entry18.grid(row=5, column=5)
        self.label19 = tk.Label(master, text='存放位置', font=('华文行楷', 12))
        self.label19.grid(row=6, column=4)
        self.entry19 = tk.Entry(master, textvariable=self.var6)
        self.entry19.grid(row=6, column=5)
        self.label20 = tk.Label(master, text='使用人', font=('华文行楷', 12))
        self.label20.grid(row=7, column=4)
        self.entry20 = tk.Entry(master, textvariable=self.var7)
        self.entry20.grid(row=7, column=5)
        self.r5 = tk.Label(master, text='出/入库', font=('华文行楷', 12))
        self.r5.grid(row=8, column=4)
        self.r6 = tk.Entry(master, textvariable=self.var8)
        self.r6.grid(row=8, column=5)
        self.bu3 = tk.Button(master, text='修改', font=('方正舒体', 12), command=self.modify)
        self.bu3.grid(row=9, column=4)
        # self.sx3 = tk.Button(master,text='刷新',font=('方正舒体',12))
        # self.sx3.grid(row=9,column=5)

        # 添加删除控件
        self.label21 = tk.Label(master, text='ID', font=('华文行楷', 12))
        self.label21.grid(row=1, column=6)
        self.entry21 = tk.Entry(master)
        self.entry21.grid(row=1, column=7)
        self.label22 = tk.Label(master, text='日期', font=('华文行楷', 12))
        self.label22.grid(row=2, column=6)
        self.entry22 = tk.Entry(master)
        self.entry22.grid(row=2, column=7)
        self.label23 = tk.Label(master, text='物品名', font=('华文行楷', 12))
        self.label23.grid(row=3, column=6)
        self.entry23 = tk.Entry(master)
        self.entry23.grid(row=3, column=7)
        self.label24 = tk.Label(master, text='规格', font=('华文行楷', 12))
        self.label24.grid(row=4, column=6)
        self.entry24 = tk.Entry(master)
        self.entry24.grid(row=4, column=7)
        self.label25 = tk.Label(master, text='数量', font=('华文行楷', 12))
        self.label25.grid(row=5, column=6)
        self.entry25 = tk.Entry(master)
        self.entry25.grid(row=5, column=7)
        self.label26 = tk.Label(master, text='存放位置', font=('华文行楷', 12))
        self.label26.grid(row=6, column=6)
        self.entry26 = tk.Entry(master)
        self.entry26.grid(row=6, column=7)
        self.label27 = tk.Label(master, text='使用人', font=('华文行楷', 12))
        self.label27.grid(row=7, column=6)
        self.entry27 = tk.Entry(master)
        self.entry27.grid(row=7, column=7)
        self.r7 = tk.Label(master, text='出/入库', font=('华文行楷', 12))
        self.r7.grid(row=8, column=6)
        self.r8 = tk.Entry(master)
        self.r8.grid(row=8, column=7)
        self.bu4 = tk.Button(master, text='删除', font=('方正舒体', 12), command=self.dele)
        self.bu4.grid(row=9, column=6)
        self.sx4 = tk.Button(master, text='刷新', font=('方正舒体', 12), command=self.refresh)
        self.sx4.grid(row=9, column=7, sticky=tk.E)  # sticky = tk.E右对齐  上北下南左西右东

    # 定义添加函数
    def insert(self):
        print(self.var.get())
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            db='test',
            port=3306)
        self.cursor = self.conn.cursor()
        # info = [self.entry0.get(),self.entry1.get(),self.entry2.get(),self.entry3.get(),self.entry4.get(),self.entry5.get(),self.entry6.get(),self.var.get()]
        # self.tree.insert('', END, values=info)  # 添加数据到末尾
        insert = "insert into sys_user(id,time,name,specification,nums,location,user,in_out)\
    VALUES('%s','%s','%s', '%s', '%d', '%s', '%s','%s')" \
                 % (self.entry0.get(), self.entry1.get(), self.entry2.get(), self.entry3.get(), int(self.entry4.get()),
                    self.entry5.get(), self.entry6.get(), self.var.get())
        try:

            self.cursor.execute(insert)
            # 执行sql语句
            self.conn.commit()
            self.tree.insert('', END,
                             values=[self.entry0.get(), self.entry1.get(), self.entry2.get(), self.entry3.get(),
                                     int(self.entry4.get()), self.entry5.get(), self.entry6.get(),
                                     self.var.get()])  # 添加数据到末尾
            print("insert ok")
        except:

            # 发生错误时回滚
            self.conn.rollback()
        finally:

            # 关闭数据库连接
            self.conn.close()

    # 定义刷新函数
    def refresh(self):
        # 将TreeView中数据清空
        for row in self.tree.get_children():
            self.tree.delete(row)
        # 将mysql中的数据显示在TreeView中
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            db='test',
            port=3306)
        self.cursor = self.conn.cursor()

        try:
            self.cursor.execute("SELECT * FROM sys_user")
            results = self.cursor.fetchall()

            for row in results:
                idd = row[0]
                time = row[1]
                name = row[2]
                specification = row[3]
                nums = row[4]
                location = row[5]
                user = row[6]
                in_out = row[7]

                self.tree.insert('', END,
                                 values=[idd, time, name, specification, nums, location, user, in_out])  # 添加数据到末尾
        except Exception as e:
            print(e)
        finally:
            self.cursor.close()
            self.conn.close()
            # 定义查询函数

    def query_bef(self, st, entryy):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            db='test',
            port=3306)
        self.cursor = self.conn.cursor()
        query = "select * from sys_user where %s = '%s'" % (st, entryy)  # 查询
        try:
            self.cursor.execute(query)
            # 获取所有记录列表
            results = self.cursor.fetchall()
            for row in results:
                idd = row[0]
                time = row[1]
                name = row[2]
                specification = row[3]
                nums = row[4]
                location = row[5]
                user = row[6]
                in_out = row[7]
                self.tree.insert('', END,
                                 values=[idd, time, name, specification, nums, location, user, in_out])  # 添加数据到末尾
            # 打印结果

            # print ("idd = %s,time = %s,name=%s,specification=%s,nums=%d,location=%s,user=%s,in_out=%s" % \
            #      (idd,time,name, specification, nums, location, user, in_out ))
        except Exception as e:
            print(e)

        finally:
            self.conn.close()
            self.cursor.close()

    def query(self):
        if self.entry7.get():
            self.query_bef('id', self.entry7.get())
        elif self.entry8.get():
            self.query_bef('time', self.entry8.get())
        elif self.entry9.get():
            self.query_bef('name', self.entry9.get())
        elif self.entry10.get():
            self.query_bef('specification', self.entry10.get())
        elif self.entry11.get():
            self.query_bef('nums', self.entry11.get())
        elif self.entry12.get():
            self.query_bef('location', self.entry12.get())
        elif self.entry13.get():
            self.query_bef('user', self.entry13.get())
        else:
            self.query_bef('in_out', self.r4.get())

    # 绑定的单击函数
    def click_bf(self, event):  # 单击

        for item in self.tree.selection():
            item_text = self.tree.item(item, "values")
            # print(item_text)#输出所选行的第一列的值
            self.var1.set(item_text[0])
            self.var2.set(item_text[1])
            self.var3.set(item_text[2])
            self.var4.set(item_text[3])
            self.var5.set(item_text[4])
            self.var6.set(item_text[5])
            self.var7.set(item_text[6])
            self.var8.set(item_text[7])

    # 定义修改函数
    def modify_be(self, ss, en, nu):
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            db='test',
            port=3306)
        self.cursor = self.conn.cursor()
        change = "update sys_user set %s = '%s' where id = '%s'" % (ss, en, nu)  # 查询
        try:

            # 执行SQL语句
            self.cursor.execute(change)
            # 获取所有记录列表
            self.conn.commit()
        except Exception as e:
            print(e)

        finally:
            self.cursor.close()
            self.conn.close()

    def modify(self):
        self.modify_be('time', self.entry15.get(), self.entry14.get())
        self.modify_be('name', self.entry16.get(), self.entry14.get())
        self.modify_be('specification', self.entry17.get(), self.entry14.get())
        self.modify_be('nums', self.entry18.get(), self.entry14.get())
        self.modify_be('location', self.entry19.get(), self.entry14.get())
        self.modify_be('user', self.entry20.get(), self.entry14.get())
        self.modify_be('in_out', self.r6.get(), self.entry14.get())

    # 定义删除函数
    def dele(self):
        self.conn = pymysql.connect(
            host='localhost',
            user='root',
            password='123456',
            db='test',
            port=3306)
        self.cursor = self.conn.cursor()
        delete = "delete from sys_user where id ='%s'" % (self.entry21.get())  # 删除
        try:

            # 执行SQL语句
            self.cursor.execute(delete)
            # 获取所有记录列表
            self.conn.commit()
        except Exception as e:
            print(e)

        finally:
            self.cursor.close()
            self.conn.close()


root = tk.Tk()
root.title('药品管理系统')
# root.iconbitmap('fa.ico') #设置左上角小图标
root.geometry('965x562+200+100')
root.resizable(0, 0)  # 设置窗口不可变
Med(root)
root.mainloop()