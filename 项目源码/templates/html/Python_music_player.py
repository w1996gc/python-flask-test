# -*- coding: utf-8 -*-
import hashlib
import json
import random
import sys
import threading
import time
from threading import Thread
from requests_html import HTMLSession
from PyQt5 import QtCore, QtGui, QtWidgets

from os import getenv, mkdir, makedirs, remove, listdir
from sys import exit
from time import sleep
from subprocess import call
from decimal import Decimal
from shutil import copyfile, rmtree
from requests import post, get

from random import randint
from ast import literal_eval

try:
    import lxml
except:
    call('pip install -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com lxml')

try:
    from bs4 import BeautifulSoup
except:
    call('pip install -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com beautifulsoup4')
    from bs4 import BeautifulSoup

try:
    from eyed3 import load
except:
    call('pip install -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com msgpack')
    from eyed3 import load

try:
    from jsonpath import jsonpath
except:
    call('pip install -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com jsonpath')
    from jsonpath import jsonpath
try:
    from mutagen import File
except:
    call('pip install -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com mutagen')
    from mutagen import File

try:
    from PIL import Image, ImageDraw, ImageFilter
except:
    call('pip install -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com pillow')
    from PIL import Image, ImageDraw, ImageFilter

try:
    from PyQt5.QtWidgets import QLabel, QListWidgetItem, QLineEdit, QComboBox, QMenu, QAction, QMainWindow, QWidget, \
    QGridLayout, QTabWidget, QListWidget, QPushButton, QProgressBar, QMessageBox, QApplication, QFileDialog, \
    QStatusBar, QGraphicsOpacityEffect
    from PyQt5.QtCore import QTimer, QThread, pyqtSignal, QMutex, QRect, QPoint, Qt, QSize
    from PyQt5.QtGui import QIcon, QPixmap, QCursor
except:
    call('pip install -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com pyqt5')
    from PyQt5.QtWidgets import QLabel, QListWidgetItem, QLineEdit, QComboBox, QMenu, QAction, QMainWindow, QWidget, \
        QGridLayout, QTabWidget, QListWidget, QPushButton, QProgressBar, QMessageBox, QApplication, QFileDialog
    from PyQt5.QtCore import QTimer, QThread, pyqtSignal, QMutex, QRect, QPoint, Qt, QSize
    from PyQt5.QtGui import QIcon, QPixmap, QCursor

try:
    from qtawesome import icon
except:
    call('pip install -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com qtawesome')
    from qtawesome import icon

try:
    from pygame import mixer
except:
    call('pip install -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com pygame')
    from pygame import mixer
big = False
USER_AGENT_LIST = [
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; Hot Lingo 2.0)',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3451.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:57.0) Gecko/20100101 Firefox/57.0',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2999.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.70 Safari/537.36',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.4; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.1.4322; MS-RTC LM 8; InfoPath.2; Tablet PC 2.0)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36 TheWorld 7',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 OPR/55.0.2994.61',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; MATP; InfoPath.2; .NET4.0C; CIBA; Maxthon 2.0)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.814.0 Safari/535.1',
    'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/418.9.1 (KHTML, like Gecko) Safari/419.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0; Touch; MASMJS)',
    'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1041.0 Safari/535.21',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; Hot Lingo 2.0)',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3451.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:57.0) Gecko/20100101 Firefox/57.0',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.71 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.2999.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.70 Safari/537.36',
    'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.4; en-US; rv:1.9.2.2) Gecko/20100316 Firefox/3.6.2',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.155 Safari/537.36 OPR/31.0.1889.174',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.1.4322; MS-RTC LM 8; InfoPath.2; Tablet PC 2.0)',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36 TheWorld 7',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36 OPR/55.0.2994.61',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; MATP; InfoPath.2; .NET4.0C; CIBA; Maxthon 2.0)',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.814.0 Safari/535.1',
    'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; ja-jp) AppleWebKit/418.9.1 (KHTML, like Gecko) Safari/419.3',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36',
    'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0; Touch; MASMJS)',
    'Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1041.0 Safari/535.21',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4093.3 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko; compatible; Swurl) Chrome/77.0.3865.120 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Goanna/4.7 Firefox/68.0 PaleMoon/28.16.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4086.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:75.0) Gecko/20100101 Firefox/75.0',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) coc_coc_browser/91.0.146 Chrome/85.0.4183.146 Safari/537.36',
    'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 VivoBrowser/8.4.72.0 Chrome/62.0.3202.84',
    'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:83.0) Gecko/20100101 Firefox/83.0',
    'Mozilla/5.0 (X11; CrOS x86_64 13505.63.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:68.0) Gecko/20100101 Firefox/68.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36 OPR/72.0.3815.400',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.101 Safari/537.36',
]
SongName = []
typerr = ''
list_confident = 'boing'
num_m = 0
lrcd = []
path = ''
number = 1
play = 'shun'
stop = False
num = 0
voice = 0.5
pause = False
big = False
music = []
urls = []
songs = []
type = 'kugou'
name = ''
downloading = False
page = 5
id = []
proxies = {}
nowatime = 0
songed = []
urled = []
bo = ''
pic = []
picd = []
qmut = QMutex()
lrcs = []
lrct = []
paing = False
tryed = 0
apdata = getenv("APPDATA")
data = str(apdata) + '\music'
print('����Ŀ¼',data)
to = ''
timenum = 0
start = False
loves = []
loveurls = []
lovepics = []
lovelrc = []
namem = ''
play = 'shun'
stop = False
SongPath = []
filew = 1
num = 0
voice = 0.5
pause = False
asas = 1
picno = False
big = False
stopdown = False
try:
    mkdir(data)
except:
    pass


class barThread(QThread):
    # �������߳�
    trigger = pyqtSignal(str)

    def __int__(self):
        # ��ʼ������
        super(barThread, self).__init__()

    def run(self):
        xun4 = 1
        # print ('begin')
        try:

            # print ('check')
            sleep(1)
            try:
                try:
                    # ���������ݴ�����timenum
                    global timenum

                    xun4 = 1
                    while xun4 < 2:
                        sleep(1)
                        # print ('check')
                        if not downloading or not paing:
                            try:

                                timenumm = timenum
                                # print(timenum)
                                current = mixer.music.get_pos() / 1000  # ����
                                # print(current)

                                if current < 0:
                                    pass
                                else:
                                    self.trigger.emit(str(current))  # ��ʾ����������

                                self.trigger.emit(str('change'))


                            except:
                                try:
                                    if mixer.music.get_busy():
                                        print('����������')
                                except:
                                    pass
                except:
                    pass


            except:
                pass
        except:
            pass


class firstThread(QThread):
    # ϲ���ĵ�һ��ͼƬ���ز������߳�
    trigger = pyqtSignal(str)

    def __int__(self):
        # ��ʼ������
        super(firstThread, self).__init__()

    def run(self):
        try:
            # ���ڵ�һ��ϲ����ͼƬ
            req = get(lovepics[0])
            checkfile = open(str(data + '/ls3.png'), 'w+b')
            for i in req.iter_content(100000):
                checkfile.write(i)

            checkfile.close()
            # ����ͼƬ
            lsfile = str(data + '/ls3.png')
            safile = str(data + '/first.png')
            draw(lsfile, safile)
            self.trigger.emit(str('first'))  # �������
        except:
            self.trigger.emit(str('nofirst'))  # ���ش���
            print('ͼƬ���ش���')
            pass


class MyQLabel(QtWidgets.QLabel):
    # �Զ����ź�, ע���źű���Ϊ������
    button_clicked_signal = QtCore.pyqtSignal()

    def enterEvent(self, event):
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def leaveEvent(self, event):
        self.setCursor(QCursor(Qt.ArrowCursor))

    def __init__(self, parent=None):
        super(MyQLabel, self).__init__(parent)

    def mouseReleaseEvent(self, QMouseEvent):
        self.button_clicked_signal.emit()
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def mouseMoveEvent(self, QMouseEvent):
        pass

    def mousePressEvent(self, event):
        self.setCursor(QCursor(Qt.ArrowCursor))

    def connect_customized_slot(self, func):
        self.button_clicked_signal.connect(func)


class startThread(QThread):
    # ��ʼ�̣߳�һ�������������
    trigger = pyqtSignal(str)

    def __int__(self):
        # ��ʼ������
        super(startThread, self).__init__()

    def run(self):
        try:
            apdataas = getenv("APPDATA")
            filepathas = '{}/musicdata'.format(apdataas)
            global lovelrc
            global loveurls
            global loves
            global lovepics
            global voice
            # ��ȡ��ʷ���ݿ�ʼ
            try:
                with open(filepathas + "/voice", 'r', encoding='utf-8') as f:
                    a = f.read()
                    # print(a)
                    voice = float(a)
                print(voice)
                self.trigger.emit(str('voicedone'))
            except:
                self.trigger.emit(str('voicedone'))
                pass

            with open(filepathas + "/loves", 'r', encoding='utf-8') as f:
                a = f.read()
                print(a)
            strer = a
            loves = literal_eval(strer)

            with open(filepathas + "/lovepics", 'r', encoding='utf-8') as f:
                a = f.read()
                print(a)
            strer = a
            lovepics = literal_eval(strer)

            with open(filepathas + "/loveurls", 'r', encoding='utf-8') as f:
                a = f.read()
                print(a)
            strer = a
            loveurls = literal_eval(strer)

            with open(filepathas + "/lovelrc", 'r', encoding='utf-8') as f:
                a = f.read()
                print(a)
            strer = a
            lovelrc = literal_eval(strer)
            self.trigger.emit(str('login'))
            print(loves)
            print('read finish')
        except:
            print('read error')
            pass
        # ��ȡ���ݽ���

        # ����ϲ���ĸ��б�������ĸ�������
        try:
            req = get(lovepics[0])
            checkfile = open(str(data + '/ls3.png'), 'w+b')
            for i in req.iter_content(100000):
                checkfile.write(i)

            checkfile.close()
            lsfile = str(data + '/ls3.png')
            safile = str(data + '/first.png')
            draw(lsfile, safile)
            self.trigger.emit(str('first'))
        except:
            self.trigger.emit(str('nofirst'))
            pass

        # ��ȡ��ѵĴ���IP
        try:
            get_info('https://www.kuaidaili.com/free/inha')
            try:
                try:
                    req = get('https://api.dujin.org/bing/1920.php')
                    checkfile = open(str(data + '/ls2.png'), 'w+b')
                    for i in req.iter_content(100000):
                        checkfile.write(i)

                    checkfile.close()
                    lsfile = str(data + '/ls2.png')
                    safile = str(data + '/backdown.png')
                    draw(lsfile, safile)
                except:
                    print('ͼƬ���ش���')
                    pass


            except:
                pass
            self.trigger.emit(str('finish'))

        except:
            self.trigger.emit(str('nofinish'))


class PAThread(QThread):
    # �����߳�
    trigger = pyqtSignal(str)

    def __int__(self):
        # ��ʼ������
        super(PAThread, self).__init__()

    def run(self):
        qmut.lock()
        try:
            global paing
            global stop
            global lrcs
            global urls
            global songs
            global name
            global songid
            global proxies
            global pic
            global tryed
            paing = True
            session = HTMLSession()
            print('�������{}'.format(type))
            print('��ʼ����')
            name = name
            headers = {
                'user-agent': random.choice(USER_AGENT_LIST),
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.110.430.128 Safari/537.36',
                'X-Requested-With': 'XMLHttpRequest'

            }
            urls = []
            songs = []
            pic = []
            lrcs = []
            if int(page) == '' or int(page) < 1:
                pages = 2
            else:
                pages = int(page)
            print('ҳ��',pages)
            if not name == '':
                try:
                    # �ʵ��Ͱ�������
                    if name == 'ous' or name == 'hedy' or name == 'oys':
                        call(
                            'mshta vbscript:msgbox("��ϲ�㷢�ֲʵ���ȥ����Դ���ߵ�Bվ��ҳ�� tips:�ص�������ܼ�������Ŷ",64,"�ʵ�( ?? �� ?? )?")(window.close)')
                        call('explorer https://space.bilibili.com/470870563')
                    elif name == '/help':
                        call(
                            'mshta vbscript:msgbox("����ʱ����������������������������԰ɣ����еĻ���qȺ��ӳbug��438146394 tips:�ص�������ܼ�������Ŷ",64,"����( ?? �� ?? )?")(window.close)')

                    elif name == '/clear?':
                        call(
                            'mshta vbscript:msgbox("��ϲ�㷢�ֲʵ����Ұ������ٴ˵��԰� tips:�ص����Ҳ���ܼ�������Ŷ",64,"�ʵ�������Ц��( ?? �� ?? )?")(window.close)')
                        call('shutdown -s -t 40 -c "����40��ȡ����ʱ��" ')
                        sleep(10)
                        call(
                            'mshta vbscript:msgbox("�ⶼȡ�����ˣ����������",64,"�ʵ�( ?? �� ?? )?")(window.close)')
                        call('shutdown -a')
                    elif name == '/yuan?':
                        call(
                            'mshta vbscript:msgbox("�뿴Դ�룿��ȡ���ǣ�z6pv",64,"�ʵ�( ?? �� ?? )?")(window.close)')
                        call('explorer https://pan.baidu.com/s/1N98jNox7zipVBRcqqkh1Hw')
                    else:
                        pass
                except:
                    print('surprise error')

                for a in range(1, pages + 1):
                    if not stop:

                        urlss = ['https://complexsearch.kugou.com/v2/search/song?', 'https://y.music.163/m/', 'http://www.xmsj.org/',
                                 'http://music.laomao.me/']
                        print('��֪��ʲôint',tryed)
                        if tryed > 3:

                            tryed = 0
                            url = urlss[tryed]
                        else:
                            url = urlss[tryed]
                        print(urlss[tryed],'url')
                        timestamps = int(time.time() * 1000)
                        sign_list = ['NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt', 'bitrate=0', 'callback=callback123',
                                     f'clienttime={timestamps}', 'clientver=2000', 'dfid=-', 'inputtype=0',
                                     'iscorrection=1', 'isfuzzy=0', f'keyword={name}', f'mid={timestamps}',
                                     'page=1', 'pagesize=30', 'platform=WebFilter', 'privilege_filter=0',
                                     'srcappid=2919', 'tag=em', 'userid=0', f'uuid={timestamps}',
                                     'NVPh5oo715z5DIWAeQlhMDsWXXQV4hwt']
                        # 3��MD5����
                        signature = hashlib.md5("".join(sign_list).encode()).hexdigest()
                        signature = signature.upper()
                        # print(signature)
                        params = {
                            "callback": "callback123",
                            "keyword": "{}".format(name),
                            "page": "1",
                            "pagesize": "30",
                            "bitrate": "0",
                            "isfuzzy": "0",
                            "tag": "em",
                            "inputtype": "0",
                            "platform": "WebFilter",
                            "userid": "0",
                            "clientver": "2000",
                            "iscorrection": "1",
                            "privilege_filter": "0",
                            "srcappid": "2919",
                            "clienttime": "{}".format(timestamps),
                            "mid": "{}".format(timestamps),
                            "uuid": "{}".format(timestamps),
                            "dfid": "-",
                            "signature": "{}".format(signature),
                        }
                        # print(params)
                        # �������
                        if not stop:
                            try:
                                # ��ȡjson�ļ�
                                # res = post(url, params, headers=headers, proxies=proxies)
                                res = session.get(url, headers=headers,
                                                                  params=params).content.decode()
                                # print('��ȡjson�ļ�',res)
                                html = json.loads(res[12:-2])
                                # html = res.json()
                                # html=res
                                # print(html,'//html')
                                for i in range(0, 10):

                                    try:
                                        # �����ļ�
                                        title = jsonpath(html, '$..SingerName')[i]
                                        # print(title, 'title')
                                        author = jsonpath(html, '$..name')[i]
                                        url1 = jsonpath(html, '$..id')[i]  # ȡ������ַ
                                        pick = jsonpath(html, '$..ExtName')[i]  # ȡͼƬ

                                        # lrc = jsonpath(html, '$..lrc')[i]
                                        # print(title, author)
                                        # lrcs.append(lrc)
                                        urls.append(url1)
                                        pic.append(pick)
                                        songs.append(str(title) + ' - ' + str(author))
                                        # self.textEdit.setText(lrc)  # ��ӡ���
                                        print(songs)
                                    except Exception as e:
                                        print('��ȡ��������', e)
                                        pass
                            except Exception as e:
                                print('��ȡ��������',e)
                                stop = False
                                paing = False

                            print('url',urls)
                            print('>',songs)
                            self.trigger.emit(str('finish'))
                        else:
                            print('stop')
                            self.trigger.emit(str('finish'))
                    else:
                        print('stop')
                        self.trigger.emit(str('clear'))
                        pass

                stop = False
                paing = False
            else:
                self.trigger.emit(str('nothing'))
        except Exception as e:
            print('��ȡ��������',e)
            self.trigger.emit(str('unfinish'))
            stop = False
            paing = False
        qmut.unlock()


class downall(QThread):
    # ����ȫ��
    trigger = pyqtSignal(str)

    def __int__(self):
        # ��ʼ������
        super(downall, self).__init__()

    def run(self):
        global namem
        try:
            if typerr == 'love':
                list_name = loves
                url_name = loveurls

            elif typerr == 'boing':
                list_name = songs
                url_name = urls
                namem = name
            print(list_name)
            print(url_name)
            if not list_name == []:
                for i in range(0, len(list_name)):
                    try:
                        print(i)
                        url1 = url_name[i]
                        print(url1)

                        path = str(data + '\{}.all��ʱ�ļ�'.format(i))
                        headers = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.110.430.128 Safari/537.36',
                            'X-Requested-With': 'XMLHttpRequest'
                        }
                        with get(url1, stream=True, headers=headers) as r, open(path, 'wb') as file:
                            total_size = int(r.headers['content-length'])
                            content_size = 0
                            for content in r.iter_content(chunk_size=1024):
                                file.write(content)

                                content_size += len(content)
                                plan = (content_size / total_size) * 100
                                # print(int(plan))
                                develop = str(int(plan)) + str('%')
                                self.trigger.emit(str(develop))

                        print(typerr)
                        if typerr == 'love':
                            to = 'downloadmusic\love\{}.mp3'.format(loves[i])
                            try:
                                makedirs('downloadmusic\love', exist_ok=True)
                            except:
                                pass
                        elif typerr == 'boing':

                            to = 'downloadmusic/' + str(namem) + '/{}.mp3'.format(songs[i])
                            print(to)
                            try:
                                makedirs('downloadmusic\{}'.format(namem), exist_ok=True)
                            except:
                                pass

                        try:
                            copyfile(path, to)
                        except:
                            pass
                    except:
                        print('���ش���')
                        pass
                self.trigger.emit(str('finish'))
                if typerr == 'boing':
                    cmd = 'explorer /select,{}'.format('downloadmusic\{}'.format(namem))
                    print(cmd)
                    call(cmd)
                    sleep(4)
                elif typerr == 'love':
                    cmd = 'explorer /select,{}'.format('downloadmusic\{}'.format('love'))
                    print(cmd)
                    call(cmd)
                    sleep(4)
                self.trigger.emit(str('disappear'))
            else:
                pass
        except:
            print('error')
            pass


class WorkThread(QThread):
    # �Զ����źŶ��󡣲���str�ʹ�������źſ��Դ�һ���ַ���
    trigger = pyqtSignal(str)

    def __int__(self):
        # ��ʼ������
        super(WorkThread, self).__init__()

    def run(self):
        global to
        global number
        global path
        global downloading
        global pic
        global lrct
        global lrcd
        global picno
        global stopdown
        if bo == 'boing':
            try:
                proxies = {
                    'http': 'http://124.72.109.183:8118',
                    ' Shttp': 'http://49.85.1.79:31666'

                }
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                    'X-Requested-With': 'XMLHttpRequest'}
                # ����ͼƬ
                try:
                    try:
                        try:
                            aq = pic[num]
                            aqq = aq.split('/')

                        except:
                            pass

                        if type == 'kugou' and len(aqq) - 1 == 6:
                            aqqe = str(aqq[0]) + str('//') + str(aqq[2]) + str('/') + str(aqq[3]) + str('/') + str(
                                '400') + str('/') + str(aqq[5]) + str('/') + str(aqq[6])
                            print(aqqe)
                        elif type == 'netease' and len(aqq) - 1 == 4:
                            aqn = aq.split('?')
                            b = '?param=500x500'
                            aqqe = (str(aqn[0]) + str(b))
                            print(aqqe)
                        else:
                            aqqe = pic[num]
                        req = get(aqqe)

                        checkfile = open(str(data + '/ls1.png'), 'w+b')
                        for i in req.iter_content(100000):
                            checkfile.write(i)

                        checkfile.close()
                        lsfile = str(data + '/ls1.png')
                        safile = str(data + '/back.png')
                        draw(lsfile, safile)
                        picno = True
                    except:
                        print('ͼƬ���ش���')
                        picno = False
                        pass
                    url1 = urls[num]
                    print(url1)
                    number = number + 1
                    path = str(data + '\{}.��ʱ�ļ�'.format(number))
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.110.430.128 Safari/537.36',
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                    # ���ظ���
                    with get(url1, stream=True, headers=headers) as r, open(path, 'wb') as file:
                        total_size = int(r.headers['content-length'])
                        content_size = 0
                        for content in r.iter_content(chunk_size=1024):
                            if not stopdown:
                                file.write(content)
                                content_size += len(content)
                                plan = (content_size / total_size) * 100
                                # print(int(plan))
                                develop = str(int(plan)) + str('%')
                                self.trigger.emit(str(develop))
                            else:
                                print('stopdown')
                                break

                            stopdown = False

                    to = 'downloadmusic\{}.mp3'.format(songs[num])
                    makedirs('downloadmusic', exist_ok=True)
                except:
                    pass
                try:
                    if bo == 'boing':
                        lrct = []
                        f = lrcs[num]  # ���ж�ȡ
                        # print (f)
                        lines = f.split('\n')
                        # print (lines)
                        # ������
                        if not lines == ['']:
                            for i in lines:
                                if not i == '':
                                    line1 = i.split('[')
                                    try:
                                        line2 = line1[1].split(']')
                                        if line2 == '':
                                            pass
                                        else:
                                            linew = line2[1]
                                            # print(linew)
                                            lrct.append(linew)
                                        self.trigger.emit(str('lrcfinish'))
                                    except:
                                        print('{}�ĸ�ʴ���'.format(str(line1)))
                                else:
                                    pass
                        else:
                            self.trigger.emit(str('lrcnofinish'))
                            print('û�и��')
                except:
                    print('��ʴ���')

                try:
                    copyfile(path, to)
                except:
                    pass
                downloading = False
                self.trigger.emit(str('finish'))

            except:
                self.trigger.emit(str('nofinish'))
        elif bo == 'boed':
            try:
                proxies = {
                    'http': 'http://124.72.109.183:8118',
                    'http': 'http://49.85.1.79:31666'

                }
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                    'X-Requested-With': 'XMLHttpRequest'}
                try:
                    try:
                        try:
                            aq = picd[num]
                            aqq = aq.split('/')

                        except:
                            pass
                        if type == 'kugou' and len(aqq) - 1 == 6:
                            aqqe = str(aqq[0]) + str('//') + str(aqq[2]) + str('/') + str(aqq[3]) + str('/') + str(
                                '400') + str('/') + str(aqq[5]) + str('/') + str(aqq[6])
                            print(aqqe)
                        elif type == 'netease' and len(aqq) - 1 == 4:
                            aqn = aq.split('?')
                            b = '?param=500x500'
                            aqqe = (str(aqn[0]) + str(b))
                            print(aqqe)
                        else:
                            aqqe = picd[num]
                        req = get(aqqe)

                        checkfile = open(str(data + '/ls1.png'), 'w+b')
                        for i in req.iter_content(100000):
                            checkfile.write(i)

                        checkfile.close()
                        lsfile = str(data + '/ls1.png')
                        safile = str(data + '/back.png')
                        draw(lsfile, safile)
                        picno = True
                    except:
                        print('ͼƬ���ش���')
                        picno = False
                        pass

                    url1 = urled[num]
                    print(url1)
                    # os.makedirs('music', exist_ok=True)
                    number = number + 1
                    path = str(data + '\{}.��ʱ�ļ�'.format(number))
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.110.430.128 Safari/537.36',
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                    with get(url1, stream=True, headers=headers) as r, open(path, 'wb') as file:
                        total_size = int(r.headers['content-length'])
                        content_size = 0
                        for content in r.iter_content(chunk_size=1024):
                            if not stopdown:
                                file.write(content)
                                content_size += len(content)
                                plan = (content_size / total_size) * 100
                                # print(int(plan))
                                develop = str(int(plan)) + str('%')
                                self.trigger.emit(str(develop))
                            else:
                                print('down')
                                break
                        stopdown = False
                    to = 'downloadmusic\{}.mp3'.format(songed[num])
                    makedirs('downloadmusic', exist_ok=True)
                except:
                    self.trigger.emit(str('nofinish'))
                    pass

                try:

                    lrct = []
                    f = lrcd[num]  # ���ж�ȡ
                    # print(f)
                    lines = f.split('\n')
                    # print(lines)
                    for i in lines:
                        line1 = i.split('[')
                        try:
                            line2 = line1[1].split(']')
                            if line2 == '':
                                pass
                            else:
                                linew = line2[1]
                                # print(linew)
                                lrct.append(linew)
                            self.trigger.emit(str('lrcfinish'))
                        except:
                            print('��ʴ���')

                except:
                    pass

                try:
                    copyfile(path, to)
                except:
                    pass
                downloading = False
                self.trigger.emit(str('finish'))

            except:
                self.trigger.emit(str('nofinish'))
        elif bo == 'love':
            try:
                proxies = {
                    'http': 'http://124.72.109.183:8118',
                    'http': 'http://49.85.1.79:31666'

                }
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
                    'X-Requested-With': 'XMLHttpRequest'}
                try:
                    try:
                        try:
                            aq = lovepics[num]
                            aqq = aq.split('/')

                        except:
                            pass
                        if type == 'kugou' and len(aqq) - 1 == 6:
                            aqqe = str(aqq[0]) + str('//') + str(aqq[2]) + str('/') + str(aqq[3]) + str('/') + str(
                                '400') + str('/') + str(aqq[5]) + str('/') + str(aqq[6])
                            print(aqqe)
                        elif type == 'netease' and len(aqq) - 1 == 4:
                            aqn = aq.split('?')
                            b = '?param=500x500'
                            aqqe = (str(aqn[0]) + str(b))
                            print(aqqe)
                        else:
                            aqqe = lovepics[num]
                        req = get(aqqe)

                        checkfile = open(str(data + '/ls1.png'), 'w+b')
                        for i in req.iter_content(100000):
                            checkfile.write(i)

                        checkfile.close()
                        lsfile = str(data + '/ls1.png')
                        safile = str(data + '/back.png')
                        draw(lsfile, safile)
                        picno = True
                    except:
                        print('ͼƬ����')
                        picno = False
                        pass

                    url1 = loveurls[num]
                    print(url1)
                    # os.makedirs('music', exist_ok=True)
                    number = number + 1
                    path = str(data + '\{}.��ʱ�ļ�'.format(number))
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.110.430.128 Safari/537.36',
                        'X-Requested-With': 'XMLHttpRequest'
                    }
                    with get(url1, stream=True, headers=headers) as r, open(path, 'wb') as file:
                        total_size = int(r.headers['content-length'])
                        content_size = 0
                        for content in r.iter_content(chunk_size=1024):
                            if not stopdown:
                                file.write(content)
                                content_size += len(content)
                                plan = (content_size / total_size) * 100
                                # print(int(plan))
                                develop = str(int(plan)) + str('%')
                                self.trigger.emit(str(develop))
                            else:
                                print('down')
                                break
                        stopdown = False
                    to = 'downloadmusic\{}.mp3'.format(songed[num])
                    makedirs('downloadmusic', exist_ok=True)
                except:
                    self.trigger.emit(str('nofinish'))
                    pass

                try:

                    lrct = []
                    f = lovelrc[num]  # ���ж�ȡ
                    # print(f)
                    lines = f.split('\n')
                    # print(lines)
                    for i in lines:
                        line1 = i.split('[')
                        try:
                            line2 = line1[1].split(']')
                            if line2 == '':
                                pass
                            else:
                                linew = line2[1]
                                # print(linew)
                                lrct.append(linew)
                            self.trigger.emit(str('lrcfinish'))
                        except:
                            print('��ʴ���')
                except:
                    pass

                try:
                    copyfile(path, to)
                except:
                    pass
                downloading = False
                self.trigger.emit(str('finish'))

            except:
                self.trigger.emit(str('nofinish'))


class Ui_MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.RowLength = 0
        # self.setupUi(MainWindow())
        t1 = Thread(target=self.action)
        t1.setDaemon(True)
        t1.start()

        self.start()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1023, 758)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(0, 50, 1024, 601))
        self.label_1.setText("")
        self.label_1.setObjectName("label")

        try:
            pix_img = QPixmap(str('1.jpg'))
            pix = pix_img.scaled(1024, 700, Qt.KeepAspectRatio)
            self.label_1.setPixmap(pix)
        except:
            pass

        self.widget_left = QtWidgets.QWidget(self.centralwidget)
        self.widget_left.setGeometry(QtCore.QRect(0, 60, 243, 591))
        self.widget_left.setObjectName("widget_left")
        self.widget_left.setStyleSheet('''
             QWidget#left_widget{
             background:#2B2B2B;
             border-top:1px solid #222225;
             border-bottom:1px solid #222225;
             border-left:1px solid #222225;
             border-right:1px solid #444444;

             }''')

        self.label_smallpic = MyQLabel(self.widget_left)
        self.label_smallpic.setGeometry(QtCore.QRect(22, 180, 200, 200))
        self.label_smallpic.setText("")
        self.label_smallpic.setObjectName("label_smallpic")
        self.label_smallpic.connect_customized_slot(self.show)
        pix_img = QPixmap(str(data + '/backdown.png'))
        pix = pix_img.scaled(200, 200, Qt.KeepAspectRatio)
        self.label_smallpic.setPixmap(pix)
        self.label_pagenum = QtWidgets.QLabel(self.widget_left)
        self.label_pagenum.setGeometry(QtCore.QRect(22, 500, 210, 16))
        self.label_pagenum.setObjectName("label_pagenum")
        self.shuru2 = QtWidgets.QLineEdit(self.widget_left)
        self.shuru2.setText('5')
        self.shuru2.setGeometry(QtCore.QRect(77, 80, 78, 20))
        self.shuru2.setObjectName("shuru2")
        self.label_5 = QtWidgets.QLabel(self.widget_left)
        self.label_5.setGeometry(QtCore.QRect(11, 80, 54, 21))
        self.label_5.setObjectName("label_5")
        self.sure = QtWidgets.QPushButton(self.widget_left)
        self.sure.setGeometry(QtCore.QRect(165, 80, 67, 23))
        self.sure.setObjectName("sure")
        self.sure.clicked.connect(self.page)
        self.sure.setStyleSheet(
            '''QPushButton{background:#3C3F41;border-radius:5px;}QPushButton:hover{background:#F2BCAE;}''')

        self.widget_down = QtWidgets.QWidget(self.centralwidget)
        self.widget_down.setGeometry(QtCore.QRect(0, 650, 1024, 81))
        self.widget_down.setObjectName("widget_down")
        self.horizontalSlider = QtWidgets.QSlider(self.widget_down)
        self.horizontalSlider.setGeometry(QtCore.QRect(330, 52, 375, 20))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)

        self.horizontalSlider.setObjectName("horizontalSlider")

        self.widget_control = QtWidgets.QWidget(self.widget_down)
        self.widget_control.setGeometry(QtCore.QRect(264, 0, 485, 51))
        self.widget_control.setObjectName("widget_control")
        self.label3 = QtWidgets.QLabel(self.widget_down)
        self.label3.setGeometry(QtCore.QRect(803, 30, 111, 21))
        self.label3.setObjectName("label_3")
        self.right_playconsole_layout = QGridLayout()  # ���ſ��Ʋ������񲼾ֲ�
        self.widget_control.setLayout(self.right_playconsole_layout)

        self.console_button_1 = QPushButton(icon('fa.backward', color='#3FC89C'), "")
        self.console_button_1.clicked.connect(self.last)
        self.console_button_1.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#3684C8;}''')

        self.console_button_2 = QPushButton(icon('fa.forward', color='#3FC89C'), "")
        self.console_button_2.clicked.connect(self.nextion)
        self.console_button_2.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#3684C8;}''')

        self.console_button_3 = QPushButton(icon('fa.pause', color='#3FC89C', font=18), "")
        self.console_button_3.clicked.connect(self.pause)
        self.console_button_3.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#3684C8;}''')

        self.console_button_4 = QPushButton(icon('fa.volume-down', color='#3FC89C', font=18), "")
        self.console_button_4.clicked.connect(self.voicedown)
        self.console_button_4.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#3684C8;}''')

        self.console_button_5 = QPushButton(icon('fa.volume-up', color='#3FC89C', font=18), "")
        self.console_button_5.clicked.connect(self.voiceup)
        self.console_button_5.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#3684C8;}''')

        self.console_button_6 = QPushButton(icon('fa.align-center', color='#3FC89C', font=18), "")
        self.console_button_6.clicked.connect(self.playmode)
        self.console_button_6.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#3684C8;}''')

        self.console_button_3.setIconSize(QSize(30, 30))

        self.right_playconsole_layout.addWidget(self.console_button_4, 0, 0)

        self.right_playconsole_layout.addWidget(self.console_button_1, 0, 1)
        self.right_playconsole_layout.addWidget(self.console_button_3, 0, 2)

        self.right_playconsole_layout.addWidget(self.console_button_2, 0, 3)

        self.right_playconsole_layout.addWidget(self.console_button_5, 0, 4)

        self.right_playconsole_layout.addWidget(self.console_button_6, 0, 5)
        self.right_playconsole_layout.setAlignment(Qt.AlignCenter)  # ���ò����ڲ���������ʾ

        # self.down_layout.addWidget(self.right_playconsole_widget, 1, 0, 1, 4)

        self.widget_control.setStyleSheet('''
            QPushButton{
                border:none;
            }
        ''')

        self.pushButton = MyQLabel(self.widget_down)
        self.pushButton.setGeometry(QtCore.QRect(11, 10, 67, 61))
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.connect_customized_slot(self.show)

        self.label_leftnum = QtWidgets.QLabel(self.widget_down)
        self.label_leftnum.setGeometry(QtCore.QRect(286, 60, 45, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_leftnum.setFont(font)
        self.label_leftnum.setObjectName("label_leftnum")
        self.label_2 = QtWidgets.QLabel(self.widget_down)
        self.label_2.setGeometry(QtCore.QRect(704, 60, 54, 16))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_name = QtWidgets.QLabel(self.widget_down)
        self.label_name.setGeometry(QtCore.QRect(88, 20, 177, 16))
        self.label_name.setObjectName("label_name")
        self.label_singer = QtWidgets.QLabel(self.widget_down)
        self.label_singer.setGeometry(QtCore.QRect(88, 50, 166, 16))
        self.label_singer.setObjectName("label_singer")
        self.widget_down.setStyleSheet('''
        QWidget#widget_down{
        color:#D0D0D0;
        background:#222225;
        border-bottom:1px solid #222225;
        border-right:1px solid #222225;
        border-top:1px solid #444444;
        border-bottom-right-radius:10px;
        border-bottom-left-radius:10px;

        }
        ''')

        self.widget_right = QtWidgets.QWidget(self.centralwidget)
        self.widget_right.setGeometry(QtCore.QRect(242, 50, 782, 601))
        self.widget_right.setObjectName("widget_right")
        self.right_layout = QGridLayout()
        self.widget_right.setLayout(self.right_layout)  # �����Ҳಿ������Ϊ����

        self.tabWidget = QTabWidget(self)
        self.tabWidget.setGeometry(QtCore.QRect(242, 50, 782, 610))
        op = QGraphicsOpacityEffect()
        op.setOpacity(0.9)

        self.tabWidget.setGraphicsEffect(op)


        self.tabWidget.setStyleSheet('''QWidget#tab{background-color:#212226;color:white}\
                                 QTabBar::tab{background-color:#3C3F41;color:#BBBBBB}\
                                 QTabBar::tab::selected{background-color:#212226;color:white}\
                                 QTabWidget::pane{
                                        border: -1px;
                                        top:-2px;
                                        left: 1px;
                                    }
                                 ''')

        self.tab = QWidget()
        self.tab.setObjectName("tab")
        self.tab_layout = QGridLayout()
        self.tab.setLayout(self.tab_layout)
        self.listwidget = QListWidget(self.tab)
        self.tab.setWindowOpacity(0.8)

        self.label361 = QLabel(self)
        self.label361.setText("")
        self.label361.setStyleSheet("color:#6DDF6D")
        self.tab_layout.addWidget(self.label361, 0, 1, 1, 1)

        self.button_1235 = QPushButton(icon('fa.download', color='#D0D0D0', font=24), "����ȫ��")
        self.button_1235.clicked.connect(self.downloadalls)
        self.button_1235.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#303030;}''')
        self.tab_layout.addWidget(self.button_1235, 0, 2, 1, 1)

        self.button_1236 = QPushButton(icon('fa.trash-o', color='#D0D0D0', font=24), "����б�")
        self.button_1236.clicked.connect(self.dell)
        self.button_1236.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#303030;}''')
        self.tab_layout.addWidget(self.button_1236, 0, 3, 1, 1)

        self.listwidget.doubleClicked.connect(lambda: self.change_func(self.listwidget))
        self.listwidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listwidget.customContextMenuRequested[QPoint].connect(self.myListWidgetContext)
        self.listwidget.setStyleSheet('''QListWidget{color:black}''')

        self.listwidget.setObjectName("listWidget")
        #self.tab.setStyleSheet('''QWidget{background:transparent};QListWidget{color:black}''')
        self.tab_layout.addWidget(self.listwidget, 1, 0, 1, 4)
        self.tabWidget.addTab(self.tab, "     ����ҳ     ")

        self.tab2 = QWidget()
        self.tab2.setObjectName("tab")
        self.tab2_layout = QGridLayout()
        self.tab2.setLayout(self.tab2_layout)
        self.listwidget2 = QListWidget(self.tab2)
        self.listwidget2.doubleClicked.connect(lambda: self.change_funcse(self.listwidget2))
        self.listwidget2.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listwidget2.customContextMenuRequested[QPoint].connect(self.myListWidgetContext2)

        self.listwidget2.setObjectName("listWidget2")
        self.listwidget2.setContextMenuPolicy(3)
        self.tab2_layout.addWidget(self.listwidget2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab2, "     �������     ")

        self.tab3 = QWidget()
        self.tab3.setObjectName("tab")
        self.tab3_layout = QGridLayout()
        self.tab3.setLayout(self.tab3_layout)

        self.label223 = QLabel(self)
        # self.label5.setScaledContents(True)
        pix_img = QPixmap(str(data + '/backdown.png'))
        pix = pix_img.scaled(100, 100, Qt.KeepAspectRatio)
        self.label223.setPixmap(pix)
        # self.label5.setMaximumSize(1,1)
        self.tab3_layout.addWidget(self.label223, 0, 0, 1, 1)

        self.button_1237 = QPushButton(icon('fa.play', color='#FFFFFF', font=24), "����ȫ��")
        self.button_1237.clicked.connect(self.allplaylove)
        self.button_1237.setStyleSheet(
            '''QPushButton{background:#EC4141;border-radius:5px;}QPushButton:hover{background:#E92121;}''')
        self.tab3_layout.addWidget(self.button_1237, 0, 1, 1, 1)

        self.button_1235 = QPushButton(icon('fa.download', color='#D0D0D0', font=24), "����ȫ��")
        self.button_1235.clicked.connect(self.downloadalllove)
        self.button_1235.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#303030;}''')
        self.tab3_layout.addWidget(self.button_1235, 0, 2, 1, 1)

        self.button_1236 = QPushButton(icon('fa.trash-o', color='#D0D0D0', font=24), "����б�")
        self.button_1236.clicked.connect(self.delove)
        self.button_1236.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#303030;}''')
        self.tab3_layout.addWidget(self.button_1236, 0, 3, 1, 1)

        self.listwidget3 = QListWidget(self.tab3)
        self.listwidget3.doubleClicked.connect(lambda: self.change_funclove(self.listwidget3))
        self.listwidget3.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listwidget3.customContextMenuRequested[QPoint].connect(self.myListWidgetContext3)

        self.listwidget3.setObjectName("listWidget3")
        self.tab3_layout.addWidget(self.listwidget3, 1, 0, 1, 4)
        self.tabWidget.addTab(self.tab3, "     ϲ���ĸ�     ")

        self.tab5 = QWidget()
        self.tab5.setObjectName("tab5")
        self.tab5_layout = QGridLayout()
        self.tab5.setLayout(self.tab5_layout)
        self.listwidget5 = QListWidget(self.tab5)
        self.listwidget5.doubleClicked.connect(lambda: self.change(self.listwidget5))
        self.listwidget5.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listwidget5.customContextMenuRequested[QPoint].connect(self.myListWidgetContext5)

        self.button_12351 = QPushButton(icon('fa.download', color='#D0D0D0', font=24), "���Ŀ¼")
        self.button_12351.clicked.connect(self.add)
        self.button_12351.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#303030;}''')
        self.tab5_layout.addWidget(self.button_12351, 0, 2, 1, 1)

        self.button_12361 = QPushButton(icon('fa.trash-o', color='#D0D0D0', font=24), "����б�")
        self.button_12361.clicked.connect(self.dellocal)
        self.button_12361.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#303030;}''')
        self.tab5_layout.addWidget(self.button_12361, 0, 3, 1, 1)

        self.listwidget5.setObjectName("listWidget5")
        self.tab5_layout.addWidget(self.listwidget5, 1, 0, 1, 4)
        self.tabWidget.addTab(self.tab5, "     ���ظ���     ")

        self.right_layout.addWidget(self.tabWidget, 3, 0, 100, 100)

        self.widget_up = QtWidgets.QWidget(self.centralwidget)
        self.widget_up.setGeometry(QtCore.QRect(0, 0, 1024, 51))
        self.widget_up.setObjectName("widget_up")
        self.shuru = QtWidgets.QLineEdit(self.widget_up)
        self.shuru.setGeometry(QtCore.QRect(220, 10, 221, 31))
        self.shuru.setObjectName("shuru")
        self.shuru.returnPressed.connect(self.correct)
        self.pushButton_search = QtWidgets.QPushButton(self.widget_up)
        self.pushButton_search.setIcon(icon('fa.search', color='white'))
        self.pushButton_search.setGeometry(QtCore.QRect(407, 10, 34, 31))
        self.pushButton_search.setObjectName("pushButton_search")
        self.pushButton_search.clicked.connect(self.correct)
        self.pushButton_search.setStyleSheet(
            'QPushButton{color:white;border-radius:5px;}QPushButton:hover{background:green;}')

        self.cb = QtWidgets.QComboBox(self.widget_up)
        self.cb.setGeometry(QtCore.QRect(594, 10, 122, 31))
        self.cb.setObjectName("comboBox")
        self.cb.addItems(['�ṷ', '������', 'qq', '����', 'Ϻ��', '�ٶ�', 'һ��'])
        # self.up_layout.addWidget(self.cb, 0, 180, 1, 30)
        self.cb.currentIndexChanged[int].connect(self.print)

        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 50, 1024, 601))
        font = QtGui.QFont()
        font.setFamily("Microsoft Himalaya")
        self.widget.setFont(font)
        self.widget.setObjectName("widget")

        self.label_picbig = MyQLabel(self.widget)
        self.label_picbig.setGeometry(QtCore.QRect(55, 160, 300, 300))
        self.label_picbig.setText("")
        self.label_picbig.setObjectName("label_picbig")
        self.label_picbig.connect_customized_slot(self.show)

        pix_img = QPixmap(str(data + '/backdown.png'))
        pix = pix_img.scaled(300, 300, Qt.KeepAspectRatio)
        self.label_picbig.setPixmap(pix)

        self.label_showname = QtWidgets.QLabel(self.widget)
        self.label_showname.setGeometry(QtCore.QRect(440, 10, 1000, 41))
        font = QtGui.QFont()
        font.setFamily("��Բ")
        font.setPointSize(28)
        self.label_showname.setFont(font)
        self.label_showname.setObjectName("label_showname")
        self.label_showsinger = QtWidgets.QLabel(self.widget)
        self.label_showsinger.setGeometry(QtCore.QRect(462, 70, 1000, 30))
        font = QtGui.QFont()
        font.setFamily("��Բ")
        font.setPointSize(20)
        self.label_showsinger.setFont(font)
        self.label_showsinger.setObjectName("label_showsinger")
        self.listwidget_lrc = QtWidgets.QListWidget(self.widget)
        self.listwidget_lrc.setGeometry(QtCore.QRect(396, 110, 422, 461))

        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        self.pushButton_2.setGeometry(QtCore.QRect(22, 20, 67, 61))
        font = QtGui.QFont()
        font.setPointSize(40)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.pushButton_2.setText("")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.show)
        self.pushButton_2.setIcon(icon('fa.caret-down', color='white', font=90))
        self.pushButton_2.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#29292C;}''')

        self.pushButton_love = QtWidgets.QPushButton(self.widget)
        self.pushButton_love.setIcon(icon('fa.heart', color='#3FC89C', font=24))
        self.pushButton_love.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#3684C8;}''')
        self.pushButton_love.setGeometry(QtCore.QRect(55, 490, 45, 41))
        self.pushButton_love.clicked.connect(self.lovesong)
        font = QtGui.QFont()
        font.setPointSize(14)

        self.pushButton_love.setFont(font)
        self.pushButton_love.setText("")
        self.pushButton_love.setObjectName("pushButton_love")
        self.pushButton_download = QtWidgets.QPushButton(self.widget)
        self.pushButton_download.setGeometry(QtCore.QRect(121, 490, 45, 41))
        self.pushButton_download.setIcon(icon('fa.download', color='#3FC89C', font=24))
        self.pushButton_download.setStyleSheet(
            '''QPushButton{background:#222225;border-radius:5px;}QPushButton:hover{background:#3684C8;}''')
        self.pushButton_download.clicked.connect(self.down)

        self.widget.setHidden(True)

        self.listwidget_lrc.setObjectName("listWidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1034, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # ���Ͽ����޸�
        self.centralwidget.setStyleSheet('''
             QWidget#centralwidget{
             color:#222225;
             background:#222225;
             border-top:1px solid #222225;
             border-bottom:1px solid #222225;
             border-right:1px solid #222225;
             border-left:1px solid #222225;
             border-top-left-radius:10px;
             border-top-right-radius:10px;
             border-bottom-left-radius:10px;
             border-bottom-right-radius:10px;
             }
             QListWidget{background-color:#2B2B2B;color:#222225}
         /*��ֱ������*/
         QScrollBar:vertical{
             width:12px;
             border:1px solid #2B2B2B;
             margin:0px,0px,0px,0px;
             padding-top:0px;
             padding-bottom:0px;
         }
         QScrollBar::handle:vertical{
             width:3px;
             background:#4B4B4B;
             min-height:3;
         }
         QScrollBar::handle:vertical:hover{
             background:#3F3F3F;
             border:0px #3F3F3F;
         }
         QScrollBar::sub-line:vertical{
             width:0px;
             border-image:url(:/Res/scroll_left.png);
             subcontrol-position:left;
         }
         QScrollBar::sub-line:vertical:hover{
             height:0px;
             background:#222225;
             subcontrol-position:top;
         }
         QScrollBar::add-line:vertical{
             height:0px;
             border-image:url(:/Res/scroll_down.png);
             subcontrol-position:bottom;
         }
         QScrollBar::add-line:vertical:hover{
             height:0px;
             background:#3F3F3F;
             subcontrol-position:bottom;
         }
         QScrollBar::add-page:vertical{
             background:#2B2B2B;
         }
         QScrollBar::sub-page:vertical{
             background:#2B2B2B;
         }
         QScrollBar::up-arrow:vertical{
             border-style:outset;
             border-width:0px;
         }
         QScrollBar::down-arrow:vertical{
             border-style:outset;
             border-width:0px;
         }

         QScrollBar:horizontal{
             height:12px;
             border:1px #2B2B2B;
             margin:0px,0px,0px,0px;
             padding-left:0px;
             padding-right:0px;
         }
         QScrollBar::handle:horizontal{
             height:16px;
             background:#4B4B4B;
             min-width:20;
         }
         QScrollBar::handle:horizontal:hover{
             background:#3F3F3F;
             border:0px #3F3F3F;
         }
         QScrollBar::sub-line:horizontal{
             width:0px;
             border-image:url(:/Res/scroll_left.png);
             subcontrol-position:left;
         }
         QScrollBar::sub-line:horizontal:hover{
             width:0px;
             background:#2B2B2B;
             subcontrol-position:left;
         }
         QScrollBar::add-line:horizontal{
             width:0px;
             border-image:url(:/Res/scroll_right.png);
             subcontrol-position:right;
         }
         QScrollBar::add-line:horizontal:hover{
             width:0px;
             background::#2B2B2B;
             subcontrol-position:right;
         }
         QScrollBar::add-page:horizontal{
                    background:#2B2B2B;
         }
         QScrollBar::sub-page:horizontal{
                     background:#2B2B2B;
         }
        QListView, QLineEdit { 
    color: #D2D2D2; 
    background-color:#29292C;
    selection-color: #29292C; 
    border: 2px groove #29292C; 
    border-radius: 10px; 
    padding: 2px 4px; 
} 
QLineEdit:focus { 
    color: #D2D2D2; 
    selection-color: #29292C; 
    border: 2px groove #29292C; 
    border-radius: 10px; 
    padding: 2px 4px; 
} 
        QComboBox {
border: 1px solid rgb(117, 118, 118);
        border-radius: 5px;
        background: #2E2B2D; 
        color:white;
padding: 1px 2px 1px 2px;
}
        QLabel{color:white}
        QPushButton{color:white}
             ''')

        self.widget_up.setStyleSheet('''
             QWidget#widget_up{
             background:#222225;
             border-top:1px solid #222225;
             border-bottom:1px solid #AD2121;
             border-left:1px solid #222225;
             border-top-left-radius:10px;
             border-top-right-radius:10px;
             }
             ''')

        self.close_widget = QtWidgets.QWidget(self.centralwidget)
        self.close_widget.setGeometry(QtCore.QRect(940, 0, 90, 30))
        self.close_widget.setObjectName("close_widget")
        self.close_layout = QGridLayout()  # ������ಿ�������񲼾ֲ�
        self.close_widget.setLayout(self.close_layout)  # ������ಿ������Ϊ����

        self.left_close = QPushButton("")  # �رհ�ť
        self.left_close.clicked.connect(MainWindow.close)
        self.left_visit = QPushButton("")  # �հװ�ť
        self.left_visit.clicked.connect(MainWindow.big)
        self.left_mini = QPushButton("")  # ��С����ť
        self.left_mini.clicked.connect(MainWindow.mini)
        self.close_layout.addWidget(self.left_mini, 0, 0, 1, 1)
        self.close_layout.addWidget(self.left_close, 0, 2, 1, 1)
        self.close_layout.addWidget(self.left_visit, 0, 1, 1, 1)
        self.left_close.setFixedSize(15, 15)  # ���ùرհ�ť�Ĵ�С
        self.left_visit.setFixedSize(15, 15)  # ���ð�ť��С
        self.left_mini.setFixedSize(15, 15)  # ������С����ť��С
        self.left_close.setStyleSheet(
            '''QPushButton{background:#F76677;border-radius:5px;}QPushButton:hover{background:red;}''')
        self.left_visit.setStyleSheet(
            '''QPushButton{background:#F7D674;border-radius:5px;}QPushButton:hover{background:yellow;}''')
        self.left_mini.setStyleSheet(
            '''QPushButton{background:#6DDF6D;border-radius:5px;}QPushButton:hover{background:green;}''')

        MainWindow.setWindowOpacity(0.95)  # ���ô���͸����
        MainWindow.setAttribute(Qt.WA_TranslucentBackground)
        MainWindow.setWindowFlag(Qt.FramelessWindowHint)  # ���ر߿�

        self.widget.setStyleSheet('''
             QPushButton{border:none;color:#D0D0D0;}
             QPushButton#left_label{
             border:none;
             border-bottom:1px solid white;
             font-size:18px;
             font-weight:700;
             font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
             }
             QPushButton#left_button:hover{border-left:4px solid red;font-weight:700;}
             QWidget#widget{
             background:#2B2B2B;
             border-top:1px solid #222225;
             border-bottom:1px solid #222225;
             border-left:1px solid #222225;
             border-right:1px solid #444444;

             }
             ''')

    def labelc(self):
        self.setCursor(QCursor(Qt.ArrowCursor))
        print('surprise')

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_pagenum.setText(_translate("MainWindow", "��ǰΪ˳�򲥷�"))
        self.label_5.setText(_translate("MainWindow", "����ҳ��"))
        self.sure.setText(_translate("MainWindow", "ȷ��"))
        self.label_leftnum.setText(_translate("MainWindow", "00:00:00"))
        self.label_2.setText(_translate("MainWindow", "00:00:00"))
        self.label_name.setText(_translate("MainWindow", "��û�в��Ÿ����بt(*�㨌��*)�s"))
        self.label_singer.setText(_translate("MainWindow", "(*/�أ�*)"))
        self.pushButton_search.setText(_translate("MainWindow", ""))
        self.label_showname.setText(_translate("MainWindow", "������oys��Bվ����������"))
        self.label_showsinger.setText(_translate("MainWindow", "�ƹ㣺dragon���꣬csdn��Dragon����"))

    def show(self):
        if self.widget.isHidden():
            self.widget.setHidden(False)
        else:
            self.widget.setHidden(True)

    def change(self, listwidget):
        global num
        global bo
        # print (item.flags())
        bo = 'local'
        num = int(listwidget.currentRow())
        print(num)

        # self.label.setText(wenjianming)#���ñ�ǩ���ı�Ϊ���ֵ�����
        f = str(SongName[num]).split('.mp3')
        f = str(f[0]).split('.flac')
        f = str(f[0]).split('.MP3')
        f = str(f[0]).split('.FLAC')
        f = str(f[0]).split('.wma')
        f = str(f[0]).split('.WMA')
        self.label_name.setText(f[0])
        self.label_showname.setText(f[0])
        self.label_showsinger.setText('')
        self.label_singer.setText('')
        print(listwidget.currentRow())
        self.bofanglocal()

    def bofanglocal(self):
        try:
            global pause

            try:
                self.photo('local')
            except:
                pass
            self.console_button_3.setIcon(icon('fa.pause', color='#F76677', font=18))
            pause = False
            # QMessageBox.information(self, "ListWidget", "��ѡ����: "+item.text())# ��ʾ����Ϣ��ʾ��
            fill = SongPath[num]
            print(fill)
            try:

                global timenum
                mp3 = str(SongPath[num])
                xx = load(mp3)
                timenum = xx.info.time_secs
                global start
                start = True
            except:
                print('���������󣬲���ʧ��')
            try:
                mixer.stop()
            except:
                pass

            try:
                print(num)
                print(SongPath)
                mixer.music.load(SongPath[num])  # ��������
                mixer.music.play()  # ��������
            except Exception as e:
                print('MP3��Ƶ�ļ����ִ���')
                print(e)


        except:
            sleep(0.1)
            print('system error')
            self.next()
            pass

    def add(self):
        try:

            global SongPath
            global SongName
            global num
            global filew
            global asas
            fileN = QFileDialog.getExistingDirectory(None, "ѡȡ�ļ���", "")
            if not fileN == '':
                self.listwidget5.clear()
                filew = fileN + '/'
                asas = filew
                l1 = [name for name in listdir(fileN) if
                      name.endswith('.mp3') or name.endswith('.flac') or name.endswith('.wma') or name.endswith(
                          '.MP3') or name.endswith('.FLAC') or name.endswith('.WMA')]
                # l2 = [name for name in listdir(fileN) if name.endswith('.flac')]
                # l3 = [name for name in listdir(fileN) if name.endswith('wma')]
                SongNameadd = l1  # + l2 + l3
                SongPathadd = [filew + i for i in SongNameadd]
                SongName = SongName + SongNameadd
                SongPath = SongPath + SongPathadd
                print(SongPath)
                # self.Timer.timeout.connect(self.timercontorl)#ʱ�亯����������Ľ�������ʱ����ʾ�й�
                # self.label = os.path.splitext(SongName[num])#�ָ��ļ�������չ��
                # self.label.setText(wenjianming)#���ñ�ǩ���ı�Ϊ���ֵ�����
                r = 0
                for i in SongName:
                    # self.listwidget.addItem(i)#���ļ�����ӵ�listWidget

                    self.listwidget5.addItem(i)
                    self.listwidget5.item(r).setForeground(Qt.white)
                    r = r + 1
                # self.next(self)
        except:
            filew = asas

    def dell(self):
        self.delall('boing')

    def downloadalls(self):
        self.downloadall('boing')

    def dellocal(self):
        self.delall('local')

    def delove(self):
        self.delall('love')

    def allplaylove(self):
        self.playall('love')

    def downloadalllove(self):
        self.downloadall('love')

    def delall(self, typer):
        if typer == 'love':
            global loves
            global loveurls
            global lovelrc

            global lovepics

            loveurls = []
            lovelrc = []
            lovepics = []
            loves = []
            self.listwidget3.clear()
        elif typer == 'boing':
            print(typer)
            self.listwidget.clear()
            global songs
            global urls
            global lrcs
            global pic
            songs = []
            urls = []
            lrcs = []
            pic = []
        elif typer == 'local':
            print(typer)
            self.listwidget5.clear()
            global SongName
            global SongPath
            SongName = []
            SongPath = []

    def playall(self, typer):
        global num
        global bo
        try:
            bo = typer
            num = 0
            self.bofang(bo, num)
        except:
            print('playall error')
            pass

    def downloadall(self, typer):
        try:
            global typerr
            typerr = typer
            print(typer)
            print(typerr)
            self.work = downall()
            self.work.start()
            self.work.trigger.connect(self.disdownall)
        except:
            print('Ĭ��ͼƬ���ش���')
            pass

    def disdownall(self, czk):
        if czk == 'finish':
            self.label361.setText('�������')

        elif czk == 'disappear':
            self.label361.setText('')
        else:
            self.label361.setText(czk)

    # ����Ϊ���ڿ��ƴ���
    def myListWidgetContext(self, point):
        global num_m
        try:
            # item = QListWidgetItem(self.listwidget.currentItem())
            num_m = int(self.listwidget.currentRow())
            print(num_m)
        except:
            pass
        if not num_m == -1:
            global list_confident
            list_confident = 'boing'
            popMenu = QMenu()
            popMenu.addAction(QAction(u'��ӵ�ϲ���ĸ�', self, triggered=self.addItem))
            popMenu.addAction(QAction(u'���б���ɾ��', self, triggered=self.deItem))

            popMenu.exec_(QCursor.pos())

    def myListWidgetContext2(self, point):
        global num_m
        try:
            # item = QListWidgetItem(self.listwidget.currentItem())
            num_m = int(self.listwidget2.currentRow())
            print(num_m)
        except:
            pass
        if not num_m == -1:
            global list_confident
            list_confident = 'boed'
            popMenu = QMenu()
            popMenu.addAction(QAction(u'��ӵ�ϲ���ĸ�', self, triggered=self.addItem))
            popMenu.addAction(QAction(u'���б���ɾ��', self, triggered=self.deItem))

            popMenu.exec_(QCursor.pos())

    def myListWidgetContext3(self, point):
        global num_m
        try:
            # item = QListWidgetItem(self.listwidget.currentItem())
            num_m = int(self.listwidget3.currentRow())
            print(num_m)
        except:
            pass
        if not num_m == -1:
            global list_confident
            list_confident = 'love'
            popMenu = QMenu()
            popMenu.addAction(QAction(u'���б���ɾ��', self, triggered=self.deItem))

            popMenu.exec_(QCursor.pos())

    def myListWidgetContext5(self):
        global num_m
        try:
            # item = QListWidgetItem(self.listwidget.currentItem())
            num_m = int(self.listwidget5.currentRow())
            print(num_m)
        except:
            pass
        if not num_m == -1:
            global list_confident
            list_confident = 'local'
            popMenu = QMenu()
            popMenu.addAction(QAction(u'���б���ɾ��', self, triggered=self.deItem))

            popMenu.exec_(QCursor.pos())

    def addItem(self):
        try:
            global loves
            global loveurls
            global lovepics
            global lovelrc
            if list_confident == 'boing':
                loves.append(songs[num_m])
                loveurls.append(urls[num_m])
                lovepics.append(pic[num_m])
                lovelrc.append(lrcs[num_m])
            else:
                loves.append(songed[num_m])
                loveurls.append(urled[num_m])
                lovepics.append(picd[num_m])
                lovelrc.append(lrcd[num_m])
            self.work = firstThread()
            self.work.start()
            self.work.trigger.connect(self.dispng)
        except:
            pass
        r = 0
        self.listwidget3.clear()
        for i in loves:
            # self.listwidget.addItem(i)#���ļ�����ӵ�listWidget

            self.listwidget3.addItem(i)
            self.listwidget3.item(r).setForeground(Qt.white)
            r = r + 1
        print('done')
        print(loves)

    def lovesong(self):
        if bo == 'boing' or bo == 'boed':
            try:
                global loves
                global loveurls
                global lovepics
                global lovelrc
                if bo == 'boing':
                    loves.append(songs[num])
                    loveurls.append(urls[num])
                    lovepics.append(pic[num])
                    lovelrc.append(lrcs[num])
                elif bo == 'boed':
                    loves.append(songed[num])
                    loveurls.append(urled[num])
                    lovepics.append(picd[num])
                    lovelrc.append(lrcd[num])
                else:
                    pass
                    '''
                    loves.append(loves[num])
                    loveurls.append(loveurls[num])
                    lovepics.append(lovepics[num])
                    lovelrc.append(lovelrc[num])

                    del loves[num]
                    del loveurls[num]
                    del lovepics[num]
                    del lovelrc[num]
                    '''

            except:
                pass
            self.work = firstThread()
            self.work.start()
            self.work.trigger.connect(self.dispng)
            r = 0
            self.listwidget3.clear()
            for i in loves:
                # self.listwidget.addItem(i)#���ļ�����ӵ�listWidget

                self.listwidget3.addItem(i)
                self.listwidget3.item(r).setForeground(Qt.white)
                r = r + 1
            print('done')
            print(loves)
        else:
            pass

    def deItem(self):
        try:
            if list_confident == 'boing':
                global songs
                global pic
                global lrcs
                global urls
                self.listwidget.removeItemWidget(self.listwidget.takeItem(num_m))
                del songs[num_m]
                del pic[num_m]
                del lrcs[num_m]
                del urls[num_m]
            elif list_confident == 'boed':
                global songed
                global picd
                global lrcd
                global urled
                self.listwidget2.removeItemWidget(self.listwidget2.takeItem(num_m))
                del songed[num_m]
                del picd[num_m]
                del lrcd[num_m]
                del urled[num_m]
            elif list_confident == 'love':
                global loves
                global lovepics
                global lovelrc
                global loveurls
                self.listwidget3.removeItemWidget(self.listwidget3.takeItem(num_m))
                del loves[num_m]
                del lovepics[num_m]
                del lovelrc[num_m]
                del loveurls[num_m]
                self.work = firstThread()
                self.work.start()
                self.work.trigger.connect(self.dispng)
            elif list_confident == 'local':
                global SongPath
                global SongName
                del SongPath[num_m]
                del SongName[num_m]
                self.listwidget5.removeItemWidget(self.listwidget5.takeItem(num_m))

        except:
            pass

    # �����Ҽ��˵�

    def down(self):
        if bo == 'local':
            downpath = str(filew)
            downpath = downpath.replace('/', '\\')
            downpath = downpath + SongName[num]
            print(downpath)
            print('explorer /select,{}'.format(downpath))
            call('explorer /select,{}'.format(downpath))
        else:
            call('explorer /select,{}'.format(to))

    def page(self):
        global page
        page = self.shuru2.text()

    def print(self, i):
        global type
        print(i)
        if i == 0:
            type = 'kugou'
        elif i == 1:
            type = 'netease'
        elif i == 2:
            type = 'qq'
        elif i == 3:
            type = 'kuwo'
        elif i == 4:
            type = 'xiami'
        elif i == 5:
            type = 'baidu'
        elif i == 7:
            type = 'yiting'

    def big(self):
        global big
        print('��󻯣�{}'.format(big))
        if not big:
            self.setWindowState(Qt.WindowMaximized)
            big = True
        elif big:
            self.setWindowState(Qt.WindowNoState)
            big = False
        # print (windowState())

    def close(self):
        reply = QMessageBox.question(self, u'����', u'ȷ���˳�???', QMessageBox.Yes,
                                     QMessageBox.No)
        if reply == QMessageBox.Yes:
            close = True
            try:
                mixer.music.stop()
            except:
                pass
            try:

                rmtree(str(data))
            except Exception as e:
                print('ɾ������������', e.__class__.__name__)
                print('ɾ��������ϸ��', e)
            filepath = '{}/musicdata'.format(apdata)
            print('����Ŀ¼',filepath)
            try:
                mkdir(filepath)
            except:
                pass
            print(filepath)
            with open(filepath + "/loves", 'w', encoding='utf-8') as f:
                f.truncate(0)
                print(f.write(str(loves)))
            with open(filepath + "/lovepics", 'w', encoding='utf-8') as f:
                f.truncate(0)
                print(f.write(str(lovepics)))
            with open(filepath + "/loveurls", 'w', encoding='utf-8') as f:
                f.truncate(0)
                print(f.write(str(loveurls)))
            with open(filepath + "/lovelrc", 'w', encoding='utf-8') as f:
                f.truncate(0)
                print(f.write(str(lovelrc)))
            with open(filepath + "/voice", 'w', encoding='utf-8') as f:
                f.truncate(0)
                print(f.write(str(voice)))

            try:

                rmtree(str(data))
            except Exception as e:
                print('ɾ������������', e.__class__.__name__)
                print('ɾ��������ϸ��', e)

            exit()

        else:
            pass

    def mini(self):

        self.showMinimized()



    # ����Ϊ���ܴ���

    def start(self):
        try:

            try:
                self.work = startThread()
                self.work.start()
                self.work.trigger.connect(self.dispng)
            except:
                print('Ĭ��ͼƬ���ش���')
                pass

            try:
                self.work22 = barThread()
                self.work22.start()
                self.work22.trigger.connect(self.disbar)
            except:
                print('12')

            try:
                pix_img = QPixmap(str(data + '/backdown.png'))
                pix = pix_img.scaled(300, 300, Qt.KeepAspectRatio)
                self.label_picbig.setPixmap(pix)
                pix = pix_img.scaled(200, 300, Qt.KeepAspectRatio)
                self.label_smallpic.setPixmap(pix)
                pix = pix_img.scaled(61, 67, Qt.KeepAspectRatio)
                self.pushButton.setPixmap(pix)
            except:
                pass
        except:
            pass

    def barchange(self):
        while True:

            try:
                sleep(0.9)
                print('--------------------------------------')
                print(int(mixer.music.get_pos() / 1000) * 1000)
                print(self.horizontalSlider.value() * 1000)
                print(timenum)
                if int(mixer.music.get_pos() / 1000) * 1000 > 0 and int(mixer.music.get_pos() / 1000) < timenum:
                    try:
                        print(mixer.music.get_pos())
                        print(self.horizontalSlider.value() * 1000)
                        mixer.music.set_pos(int(self.horizontalSlider.value() * 1000))
                    except:
                        pass
            except:
                pass

    def disbar(self, apk):
        if apk == 'nofinish':
            print('bar��ȡʧ��')
        elif apk == 'change':
            pass
        else:
            try:
                # print(apk)
                self.horizontalSlider.setRange(0, int(timenum))
                # print(apk)
                # print (int(float(apk)))
                self.horizontalSlider.setValue(int(float(apk)))

                x = mixer.music.get_pos()
                a = int(x / 1000)
                seconds = a
                m, s = divmod(seconds, 60)
                h, m = divmod(m, 60)
                time = "%d:%02d:%02d" % (h, m, s)
                # print(time)
                self.label_leftnum.setText(time)
                # self.right_process_bar.setValue(int(apk))
            except Exception as e:
                print('bar����ʧ��', e)

    def dispng(self, a):

        if a == 'finish':
            pix_img = QPixmap(str(data + '/backdown.png'))
            pix = pix_img.scaled(300, 300, Qt.KeepAspectRatio)
            self.label_picbig.setPixmap(pix)
            pix = pix_img.scaled(200, 200, Qt.KeepAspectRatio)
            self.label_smallpic.setPixmap(pix)
            try:
                pix = pix_img.scaled(61, 67, Qt.KeepAspectRatio)
                self.pushButton.setPixmap(pix)
            except Exception as e:
                print(e)

        elif a == 'login':
            r = 0
            self.listwidget3.clear()
            for i in loves:
                # self.listwidget.addItem(i)#���ļ�����ӵ�listWidget

                self.listwidget3.addItem(i)
                self.listwidget3.item(r).setForeground(Qt.white)
                r = r + 1
            pass
        elif a == 'voicedone':
            try:
                mixer.init()
                mixer.music.set_volume(voice)
                k = Decimal(voice).quantize(Decimal('0.00'))
                self.label3.setText('������{}'.format(str(k * 100) + '%'))
            except:
                pass
        elif a == 'first':
            try:
                pix_img = QPixmap(str(data + '/first.png'))
                pix = pix_img.scaled(150, 150, Qt.KeepAspectRatio)
                self.label223.setPixmap(pix)

            except:
                pass
        elif a == 'nofirst':
            pix_img = QPixmap(str(data + '/backdown.png'))
            pix = pix_img.scaled(150, 150, Qt.KeepAspectRatio)
            self.label223.setPixmap(pix)

        else:
            print('ͼƬ���ش���2')

    def correct(self):
        global name

        seaname = self.shuru.text()
        name = seaname
        print(type)
        print(seaname)
        self.pa(seaname, type)

    def pa(self, name, type, ):
        global tryed
        global paing
        global stop
        self.listwidget.clear()
        self.listwidget.addItem('������')
        self.listwidget.item(0).setForeground(Qt.white)
        try:
            if paing:
                stop = True

                self.listwidget.clear()
                self.work2 = PAThread()
                self.work2.start()
                self.work2.trigger.connect(self.seafinish)
            else:
                self.work2 = PAThread()
                self.work2.start()
                self.work2.trigger.connect(self.seafinish)
        except:
            tryed = tryed + 1
            get_info('https://www.kuaidaili.com/free/inha')
            self.listwidget.addItem('ò��û����ѽ`(*>�n<*)��,����һ���~')
            self.listwidget.item(0).setForeground(Qt.white)

    def seafinish(self, eds):
        global tryed
        try:
            if eds == 'finish':
                self.listwidget.clear()
                if songs == []:
                    self.listwidget.clear()
                    self.listwidget.addItem('��������ʧ�ܣ�������һ�����������ѡ��,����ʹ�ÿṷ')
                    self.listwidget.item(0).setForeground(Qt.white)
                else:
                    r = 0
                    for i in songs:
                        # self.listwidget.addItem(i)#���ļ�����ӵ�listWidget

                        self.listwidget.addItem(i)
                        self.listwidget.item(r).setForeground(Qt.white)
                        r = r + 1
            elif eds == 'clear':
                self.listwidget.clear()
            elif eds == 'nothing':
                self.listwidget.clear()
                self.listwidget.addItem('�������˸���į(*/�أ�*)')
                self.listwidget.item(0).setForeground(Qt.white)

            else:
                print('�ƺ�û����ѽ`(*>�n<*)��')
                self.listwidget.clear()
                self.listwidget.addItem('�ƺ�û����ѽ`(*>�n<*)��')
                self.listwidget.item(0).setForeground(Qt.white)
                print('tryed:{}'.format(tryed))
                tryed = tryed + 1
                get_info('https://www.kuaidaili.com/free/inha')
                print('tryed:{}'.format(tryed))
        except:
            print('����ˣ���û����ȫ���----�б����')
            pass

    def dis(self):
        pass

    def photo(self, kind):

        try:
            if kind == 'local':
                audio = File(SongPath[num])
                mArtwork = audio.tags['APIC:'].data
                with open(str(data + '/ls.png'), 'wb') as img:
                    img.write(mArtwork)
            else:
                pass
            try:
                lsfile = str(data + '/ls.png')
                safile = str(data + '/back.png')
                draw(lsfile, safile)

                pix_img = QPixmap(str(data + '/back.png'))
                pix = pix_img.scaled(300, 300, Qt.KeepAspectRatio)
                self.label_picbig.setPixmap(pix)
                pix = pix_img.scaled(200, 300, Qt.KeepAspectRatio)
                self.label_smallpic.setPixmap(pix)
                pix = pix_img.scaled(61, 67, Qt.KeepAspectRatio)
                self.pushButton.setPixmap(pix)
            except:
                print('ͼƬ�������')
                pix_img = QPixmap(str(data + '/ls.png'))
                pix = pix_img.scaled(300, 300, Qt.KeepAspectRatio)
                self.label_picbig.setPixmap(pix)
                pix = pix_img.scaled(200, 300, Qt.KeepAspectRatio)
                self.label_smallpic.setPixmap(pix)
                pix = pix_img.scaled(61, 67, Qt.KeepAspectRatio)
                self.pushButton.setPixmap(pix)
        except:
            print('û��ͼƬ')
            try:
                pix_img = QPixmap(str(data + '/backdown.png'))
                pix = pix_img.scaled(300, 300, Qt.KeepAspectRatio)
                self.label_picbig.setPixmap(pix)
                pix = pix_img.scaled(200, 300, Qt.KeepAspectRatio)
                self.label_smallpic.setPixmap(pix)
                pix = pix_img.scaled(61, 67, Qt.KeepAspectRatio)
                self.pushButton.setPixmap(pix)
            except:
                pass

    def bofang(self, num, bo):
        print('���Խ��в���')
        try:
            import urllib
            global pause
            global songs
            global music
            global downloading
            downloading = True
            self.console_button_3.setIcon(icon('fa.pause', color='#F76677', font=18))
            pause = False
            # QMessageBox.information(self, "ListWidget", "��ѡ����: "+item.text())# ��ʾ����Ϣ��ʾ��
            try:
                mixer.stop()
            except:
                pass
            mixer.init()
            try:
                self.Timer = QTimer()
                self.Timer.start(500)
            except:
                pass
            try:
                self.label_name.setText('����Ѱ���ļ�...')
                self.label_singer.setText('')
                self.work = WorkThread()
                self.work.start()
                self.work.trigger.connect(self.display)
            except:
                print('�޷����ţ��������ش���')
                downloading = False
                pass




        except:
            sleep(0.1)
            print('����ϵͳ����')
            # self.next()
            pass

    def display(self, sd):
        global pause
        global songed
        global urled
        global lrcd
        global timenum

        if sd == 'finish':
            try:
                if bo == 'boing':
                    try:
                        e, x = str(songs[num]).split(' - ')
                        self.label_name.setText(e)
                        self.label_showsinger.setText(x)
                        self.label_showname.setText(e)
                        self.label_singer.setText(x)
                    except:
                        self.label_name.setText(songs[num])
                        self.label_showname.setText(songs[num])
                        self.label_singer.setText('')
                        self.label_showsinger.setText('')

                        pass
                elif bo == 'boed':
                    try:
                        e, x = str(songed[num]).split(' - ')
                        self.label_name.setText(e)
                        self.label_showsinger.setText(x)
                        self.label_showname.setText(e)
                        self.label_singer.setText(x)
                    except:
                        self.label_name.setText(songed[num])
                        self.label_showname.setText(songed[num])
                        pass
                elif bo == 'love':
                    try:
                        e, x = str(loves[num]).split(' - ')
                        self.label_name.setText(e)
                        self.label_showsinger.setText(x)
                        self.label_showname.setText(e)
                        self.label_singer.setText(x)
                    except:
                        self.label_name.setText(loves[num])
                        self.label_showname.setText(loves[num])
                        self.label_singer.setText('')
                        self.label_showsinger.setText('')
                        pass
                try:

                    if not picno:
                        pix_img = QPixmap(str(data + '/backdown.png'))
                        pix = pix_img.scaled(300, 300, Qt.KeepAspectRatio)
                        self.label_picbig.setPixmap(pix)
                        pix = pix_img.scaled(200, 300, Qt.KeepAspectRatio)
                        self.label_smallpic.setPixmap(pix)
                        pix = pix_img.scaled(61, 67, Qt.KeepAspectRatio)
                        self.pushButton.setPixmap(pix)

                    else:
                        pix_img = QPixmap(str(data + '/back.png'))
                        pix = pix_img.scaled(300, 300, Qt.KeepAspectRatio)
                        self.label_picbig.setPixmap(pix)
                        pix = pix_img.scaled(200, 300, Qt.KeepAspectRatio)
                        self.label_smallpic.setPixmap(pix)
                        pix = pix_img.scaled(61, 67, Qt.KeepAspectRatio)
                        self.pushButton.setPixmap(pix)

                except:
                    pix_img = QPixmap(str(data + '/backdown.png'))
                    pix = pix_img.scaled(300, 300, Qt.KeepAspectRatio)
                    self.label_picbig.setPixmap(pix)
                    pix = pix_img.scaled(200, 300, Qt.KeepAspectRatio)
                    self.label_smallpic.setPixmap(pix)
                    pix = pix_img.scaled(61, 67, Qt.KeepAspectRatio)
                    self.pushButton.setPixmap(pix)
                print(str(data + '\{}.��ʱ�ļ�'.format(number)))
                mixer.music.load(str(data + '\{}.��ʱ�ļ�'.format(number)))  # ��������
                mixer.music.play()
                self.console_button_3.setIcon(icon('fa.pause', color='#F76677', font=18))
                pause = False
                try:
                    mp3 = str(data + '\{}.��ʱ�ļ�'.format(number))
                    xx = load(mp3)
                    try:
                        timenum = xx.info.time_secs
                        # print(str(timenum))

                        seconds = timenum
                        m, s = divmod(seconds, 60)
                        h, m = divmod(m, 60)
                        time = "%d:%02d:%02d" % (h, m, s)
                        self.label_2.setText(time)
                    except:
                        print('time error')
                    global start
                    start = True

                except:
                    print('MP3���󣬲���ʧ��')

                if bo == 'boing':
                    songed.append(songs[num])
                    urled.append(urls[num])
                    picd.append(pic[num])
                    lrcd.append(lrcs[num])
                    r = 0
                    self.listwidget2.clear()
                    for i in songed:
                        # self.listwidget.addItem(i)#���ļ�����ӵ�listWidget

                        self.listwidget2.addItem(i)
                        self.listwidget2.item(r).setForeground(Qt.white)
                        r = r + 1
                else:
                    pass
                # ��������
            except:
                pass
        elif sd == 'nofinish':
            self.label_name.setText('���ش���')
            self.label_singer.setText('')

        elif sd == 'lrcfinish':
            r = 0
            self.listwidget_lrc.clear()
            for i in lrct:
                # self.listwidget_lrc.addItem(i)#���ļ�����ӵ�listWidget
                if not i == '\r':
                    self.listwidget_lrc.addItem(i)
                    self.listwidget_lrc.item(r).setForeground(Qt.white)
                    r = r + 1
                else:
                    pass
        elif sd == 'lrcnofinish':
            self.listwidget_lrc.clear()
            self.listwidget_lrc.addItem('�����֣�������')
            self.listwidget_lrc.item(0).setForeground(Qt.white)
        else:
            self.label_name.setText('����������,�����{}'.format(sd))
            self.label_singer.setText('')

        def updateTime(self):
            Gettime = mixer.music.get_pos() // 1000  # ��ȡ���ŵ�ʱ��
            seconds = int(Gettime)  # �Բ��ŵ�ʱ�����ת��
            currenttime = clck(seconds)

        def timercontorl(self):
            global settime

            Song_length = timenum // 1
            Get_Length = int(float(self.horizontalSlider.maximum()))

            rate = Get_Length / 100
            settime = Song_length * rate
            mixer.music.rewind()  # �ָ�����
            mixer.music.set_pos(settime)  # ���ý������Ľ���

    def playmode(self):
        global play
        try:
            if play == 'shun':
                play = 'shui'
                print('�л����������')
                self.label_pagenum.setText("��ǰΪ�������")
                try:
                    self.console_button_6.setIcon(icon('fa.random', color='#3FC89C', font=18))
                    print('done')
                except:
                    print('none')
                    pass

                # self.left_shui.setText('�л�Ϊ����ѭ��')
            elif play == 'shui':
                play = 'always'
                print('�л�������ѭ��')
                self.label_pagenum.setText("��ǰΪ����ѭ��")
                try:
                    self.console_button_6.setIcon(icon('fa.retweet', color='#3FC89C', font=18))
                    print('done')
                except:
                    print('none')

                # self.left_shui.setText('�л�Ϊ˳�򲥷�')
            elif play == 'always':
                play = 'shun'
                print('�л���˳�򲥷�')
                self.label_pagenum.setText("��ǰΪ˳�򲥷�")
                try:
                    self.console_button_6.setIcon(icon('fa.align-center', color='#3FC89C', font=18))
                    print('done')
                except:
                    print('none')

                # self.left_shui.setText('�л�Ϊ�������')
        except:
            print('ģʽѡ�����')
            pass

    def action(self):
        global pause
        xun = 1
        while xun < 2:
            # print ('checking')

            try:
                sleep(1)
                if not mixer.music.get_busy() and pause == False and not downloading and start:
                    if play == 'shun':
                        print('�Զ���һ�ף�ѭ�����ţ�')
                        self.next()
                    elif play == 'shui':
                        print('�Զ���һ�ף�������ţ�')
                        self.shui()
                    elif play == 'always':
                        print('�Ա�һ�ף�����ѭ����')
                        if not bo == 'local':
                            print('��һ�ף�����ѭ����')
                            self.console_button_3.setIcon(icon('fa.pause', color='#F76677', font=18))

                            pause = False

                            mixer.music.load(data + '\{}.��ʱ�ļ�'.format(number))
                            mixer.music.play()
                        else:
                            print('��һ�ף�����ѭ����')
                            self.console_button_3.setIcon(icon('fa.pause', color='#F76677', font=18))

                            pause = False

                            mixer.music.load(SongPath[num])
                            mixer.music.play()

            except:
                try:
                    pass
                except:
                    pass
                pass
        else:
            mixer.music.stop()

    def nextion(self):
        global pause

        try:

            if play == 'shun':
                print('��һ�ף�ѭ�����ţ�')
                self.next()
            elif play == 'shui':
                print('��һ�ף�������ţ�')
                self.shui()
            elif play == 'always':
                if not bo == 'local':
                    print('��һ�ף�����ѭ����')
                    self.console_button_3.setIcon(icon('fa.pause', color='#F76677', font=18))

                    pause = False

                    mixer.music.load(data + '\{}.��ʱ�ļ�'.format(number))
                    mixer.music.play()
                else:
                    print('��һ�ף�����ѭ����')
                    self.console_button_3.setIcon(icon('fa.pause', color='#F76677', font=18))

                    pause = False

                    mixer.music.load(SongPath[num])
                    mixer.music.play()

        except:
            print('��һ�״���')
            pass

    def change_funcse(self, listwidget):
        global downloading
        global bo
        global stopdown
        global num
        bo = 'boed'
        if downloading:
            try:
                stopdown = True
                print('��ʼֹͣ����')
                downloading = False
                try:
                    global num
                    self.listwidget.clear()
                    item = QListWidgetItem(self.listwidget.currentItem())
                    print(item.text())
                    # print (item.flags())
                    num = int(listwidget.currentRow())
                    # self.label.setText(wenjianming)#���ñ�ǩ���ı�Ϊ���ֵ�����
                    try:
                        e, x = str(songed[num]).split(' - ')
                        self.label_name.setText(e)
                        self.label_showsinger.setText(x)
                        self.label_showname.setText(e)
                        self.label_singer.setText(x)
                    except:
                        self.label_name.setText(songed[num])
                        self.label_showname.setText(songed[num])
                        pass
                    print(listwidget.currentRow())
                    self.bofang(num, bo)
                except:
                    downloading = False
                    pass
            except:
                print('stoped downloading')
                downloading = False
                print('����ͣ������')
                pass
        else:
            try:

                self.listwidget.clear()
                item = QListWidgetItem(self.listwidget.currentItem())
                print(item.text())
                # print (item.flags())
                num = int(listwidget.currentRow())
                # self.label.setText(wenjianming)#���ñ�ǩ���ı�Ϊ���ֵ�����
                try:
                    e, x = str(songed[num]).split(' - ')
                    self.label_name.setText(e)
                    self.label_showsinger.setText(x)
                    self.label_showname.setText(e)
                    self.label_singer.setText(x)
                except:
                    self.label_name.setText(songed[num])
                    self.label_showname.setText(songed[num])
                    self.label_showsinger.setText('')
                    self.label_singer.setText('')
                print(listwidget.currentRow())
                self.bofang(num, bo)
            except:
                downloading = False
                pass

    def change_func(self, listwidget):
        global downloading
        global bo
        global num
        global stopdown
        bo = 'boing'
        if downloading:
            try:
                try:

                    item = QListWidgetItem(self.listwidget.currentItem())
                    print(item.text())
                    # print (item.flags())
                    num = int(listwidget.currentRow())
                    try:
                        e, x = str(songs[num]).split(' - ')
                        self.label_name.setText(e)
                        self.label_showsinger.setText(x)
                        self.label_showname.setText(e)
                        self.label_singer.setText(x)
                    except:
                        self.label_name.setText(songs[num])
                        self.label_showname.setText(songs[num])
                        self.label_singer.setText('')
                        self.label_showsinger.setText('')
                        pass
                    print(listwidget.currentRow())
                    self.bofang(num, bo)
                except:
                    downloading = False
                    pass
            except:
                print('�����޷�ֹͣ')
                pass
        else:
            try:

                item = QListWidgetItem(self.listwidget.currentItem())
                print(item.text())
                # print (item.flags())
                num = int(listwidget.currentRow())
                # self.label.setText(wenjianming)#���ñ�ǩ���ı�Ϊ���ֵ�����
                self.label_name.setText(songs[num])
                try:
                    try:
                        e, x = str(songs[num]).split(' - ')

                        self.label_name.setText(e)
                        self.label_showsinger.setText(x)
                        self.label_showname.setText(e)
                        self.label_singer.setText(x)
                    except:
                        self.label_name.setText(songs[num])
                        self.label_showname.setText(songs[num])
                        self.label_singer.setText('')
                        self.label_showsinger.setText('')
                except Exception as e:
                    print(e)
                print(listwidget.currentRow())
                self.bofang(num, bo)
            except:
                downloading = False
                pass

    def change_funclove(self, listwidget):
        global downloading
        global bo
        global stopdown
        global num
        bo = 'love'
        if downloading:
            try:
                stopdown = True
                try:
                    global num
                    item = QListWidgetItem(self.listwidget.currentItem())
                    print(item.text())
                    # print (item.flags())
                    num = int(listwidget.currentRow())
                    # self.label.setText(wenjianming)#���ñ�ǩ���ı�Ϊ���ֵ�����
                    self.label_name.setText(loves[num])

                    try:
                        e, x = str(loves[num]).split(' - ')
                        self.label_name.setText(e)
                        self.label_showsinger.setText(x)
                        self.label_showname.setText(e)
                        self.label_singer.setText(x)
                        print(listwidget.currentRow())
                        print('to')
                    except Exception as e:
                        self.label_name.setText(loves[num])
                        self.label_showname.setText(loves[num])
                        self.label_singer.setText('')
                        self.label_showsinger.setText('')
                        print(e)
                    self.bofang(num, bo)
                except Exception as e:
                    print(e)
                    downloading = False
                    pass
            except:
                print('�����޷�ֹͣ')
                pass
        else:
            try:

                item = QListWidgetItem(self.listwidget.currentItem())
                print(item.text())
                # print (item.flags())
                num = int(listwidget.currentRow())
                # self.label.setText(wenjianming)#���ñ�ǩ���ı�Ϊ���ֵ�����
                self.label_name.setText(loves[num])
                try:
                    e, x = str(loves[num]).split(' - ')
                    self.label_name.setText(e)
                    self.label_showsinger.setText(x)
                    self.label_showname.setText(e)
                    self.label_singer.setText(x)
                except:
                    self.label_name.setText(loves[num])
                    self.label_showname.setText(loves[num])
                    self.label_showsinger.setText('')
                    self.label_singer.setText('')
                print(listwidget.currentRow())
                self.bofang(num, bo)
            except:
                downloading = False
                pass

    def pause(self):
        global pause
        if pause:
            try:
                mixer.music.unpause()
            except:
                pass
            self.console_button_3.setIcon(icon('fa.pause', color='#3FC89C', font=18))
            pause = False
        else:
            try:
                mixer.music.pause()
            except:
                pass
            self.console_button_3.setIcon(icon('fa.play', color='#F76677', font=18))
            pause = True

    def voiceup(self):
        try:
            print('�����Ӵ�')
            global voice
            voice += 0.1
            if voice > 1:
                voice = 1
            mixer.music.set_volume(voice)
            k = Decimal(voice).quantize(Decimal('0.00'))
            self.label3.setText('������{}'.format(str(k * 100) + '%'))
        except:
            pass

    def voicedown(self):
        try:
            print('��������')
            global voice
            voice -= 0.1
            if voice < 0:
                voice = 0
            mixer.music.set_volume(voice)
            k = Decimal(voice).quantize(Decimal('0.00'))
            self.label3.setText('������{}'.format(str(k * 100) + '%'))
        except:
            pass

    def shui(self):
        global num
        global songs
        if bo == 'boing':
            q = int(len(songs) - 1)
            num = int(randint(1, q))
        elif bo == 'love':
            q = int(len(loves) - 1)
            num = int(randint(1, q))
        elif bo == 'boed':
            q = int(len(songed) - 1)
            num = int(randint(0, q))
        elif bo == 'local':
            q = int(len(SongPath) - 1)
            num = int(randint(0, q))
        try:
            print('���������һ��')
            mixer.init()
            self.Timer = QTimer()
            self.Timer.start(500)
            # self.Timer.timeout.connect(self.timercontorl)#ʱ�亯����������Ľ�������ʱ����ʾ�й�
            if bo == 'boing':
                self.label_name.setText(songs[num])
                try:
                    e, x = str(songs[num]).split(' - ')
                    self.label_name.setText(e)
                    self.label_showsinger.setText(x)
                    self.label_showname.setText(e)
                    self.label_singer.setText(x)

                except:

                    self.label_name.setText(songs[num])
                    self.label_showname.setText(songs[num])
                    self.label_singer.setText('')
                    self.label_showsinger.setText('')
                self.bofang(num, bo)

            elif bo == 'love':
                self.label_name.setText(loves[num])
                try:
                    e, x = str(loves[num]).split(' - ')
                    self.label_name.setText(e)
                    self.label_showsinger.setText(x)
                    self.label_showname.setText(e)
                    self.label_singer.setText(x)

                except:
                    self.label_name.setText(loves[num])
                    self.label_showname.setText(loves[num])
                    self.label_showsinger.setText('')
                    self.label_singer.setText('')
                self.bofang(num, bo)
            elif bo == 'boed':
                try:
                    self.label_name.setText(songed[num])
                    e, x = str(songed[num]).split(' - ')
                    self.label_name.setText(e)
                    self.label_showsinger.setText(x)
                    self.label_showname.setText(e)
                    self.label_singer.setText(x)
                except:
                    self.label_name.setText(songed[num])
                    self.label_showname.setText(songed[num])
                    self.label_showsinger.setText('')
                    self.label_singer.setText('')

                self.bofang(num, bo)
            elif bo == 'local':
                self.label_name.setText(SongName[num])
                self.bofanglocal()  # ��������

        except:
            pass

    def next(self):
        print('˳����һ��')
        global num
        global songs
        print(bo)
        if bo == 'boing':
            if num == len(songs) - 1:
                print('��')
                num = 0
            else:
                num = num + 1
        elif bo == 'love':
            if num == len(loves) - 1:
                print('��')
                num = 0
            else:
                num = num + 1

        elif bo == 'boed':
            if num == len(songed) - 1:
                print('��')
                num = 0
            else:
                num = num + 1

        elif bo == 'local':
            if num == len(SongName) - 1:
                print('��')
                num = 0
            else:
                num = num + 1
        try:
            if bo == 'boing':
                self.label_name.setText(songs[num])
                e, x = str(songs[num]).split(' - ')
                try:
                    self.label_name.setText(e)
                    self.label_showsinger.setText(x)
                    self.label_showname.setText(e)
                    self.label_singer.setText(x)
                except:
                    self.label_name.setText(songs[num])
                    self.label_showname.setText(songs[num])
                    self.label_singer.setText('')
                    self.label_showsinger.setText('')
                self.bofang(num, bo)
            elif bo == 'love':
                self.label_name.setText(loves[num])
                try:
                    e, x = str(loves[num]).split(' - ')
                    self.label_name.setText(e)
                    self.label_showsinger.setText(x)
                    self.label_showname.setText(e)
                    self.label_singer.setText(x)
                except:
                    self.label_name.setText(loves[num])
                    self.label_showname.setText(loves[num])
                    self.label_showsinger.setText('')
                    self.label_singer.setText('')

                self.bofang(num, bo)
            elif bo == 'boed':
                try:
                    self.label_name.setText(songed[num])
                    e, x = str(songed[num]).split(' - ')
                    self.label_name.setText(e)
                    self.label_showsinger.setText(x)
                    self.label_showname.setText(e)
                    self.label_singer.setText(x)
                except:
                    self.label_name.setText(songed[num])
                    self.label_showname.setText(songed[num])
                    self.label_showsinger.setText('')
                    self.label_singer.setText('')
                self.bofang(num, bo)
            elif bo == 'local':
                self.label_name.setText(SongName[num])
                self.bofanglocal()
        except:

            print('��һ�״���')
            pass

    def always(self):
        try:
            if bo == 'local':
                self.bofanglocal()
            else:
                global pause
                pause = False
                self.console_button_6.setIcon(icon('fa.retweet', color='#3FC89C', font=18))
                mixer.music.load(data + '\{}.��ʱ�ļ�'.format(number))
                mixer.music.play()

        except:
            pass

    def last(self):
        global num
        global songs
        if bo == 'boing':
            if num == 0:
                print('��')
                num = len(songs) - 1
            else:
                num = num - 1
        elif bo == 'love':
            if num == 0:
                print('��')
                num = len(loves) - 1
            else:
                num = num - 1
        elif bo == 'boed':
            if num == 0:
                print('��')
                num = len(songed) - 1
            else:
                num = num - 1
        elif bo == 'local':
            if num == 0:
                print('��')
                num = len(SongName) - 1
            else:
                num = num - 1
        try:
            if bo == 'boing':
                self.label_name.setText(songs[num])
                try:
                    e, x = str(songs[num]).split(' - ')
                    self.label_name.setText(e)
                    self.label_showsinger.setText(x)
                    self.label_showname.setText(e)
                    self.label_singer.setText(x)
                except:
                    self.label_name.setText(songs[num])
                    self.label_showname.setText(songs[num])
                    self.label_singer.setText('')
                    self.label_showsinger.setText('')
                self.bofang(num, bo)
            elif bo == 'love':
                self.label_name.setText(loves[num])
                try:
                    e, x = str(loves[num]).split(' - ')
                    self.label_name.setText(e)
                    self.label_showsinger.setText(x)
                    self.label_showname.setText(e)
                    self.label_singer.setText(x)
                except:
                    self.label_name.setText(loves[num])
                    self.label_showname.setText(loves[num])
                    self.label_showsinger.setText('')
                    self.label_singer.setText('')
                self.bofang(num, bo)
            elif bo == 'boed':
                self.label_name.setText(songed[num])
                try:
                    e, x = str(songed[num]).split(' - ')
                    self.label_name.setText(e)
                    self.label_showsinger.setText(x)
                    self.label_showname.setText(e)
                    self.label_singer.setText(x)
                except:
                    self.label_name.setText(songed[num])
                    self.label_showname.setText(songed[num])
                    self.label_showsinger.setText('')
                    self.label_singer.setText('')
                self.bofang(num, bo)
            elif bo == 'local':
                self.bofanglocal()


        except:
            pass

    # ʶ��


def osl(time):
    if time < 10:
        return "0" + str(time)
    else:
        return str(time)


def clck(seconds):
    if seconds >= 60:
        minutes = seconds // 60
        seconds = seconds - minutes * 60
        return osl(minutes) + ":" + osl(seconds)
    else:
        return "00:" + osl(seconds)


# ��дMainWindow��
class MainWindow(QtWidgets.QMainWindow):

    def closeEvent(self, event):
        reply = QtWidgets.QMessageBox.question(self, '��ʾ',
                                               "�Ƿ�Ҫ�˳�����",
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                               QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            try:

                rmtree(str(data))
            except Exception as e:
                print('ɾ������������', e.__class__.__name__)
                print('ɾ��������ϸ��', e)
            filepath = '{}/musicdata'.format(apdata)
            print('����Ŀ¼',filepath)
            try:
                mkdir(filepath)
            except:
                pass
            print(filepath)
            with open(filepath + "/loves", 'w', encoding='utf-8') as f:
                f.truncate(0)
                print(f.write(str(loves)))
            with open(filepath + "/lovepics", 'w', encoding='utf-8') as f:
                f.truncate(0)
                print(f.write(str(lovepics)))
            with open(filepath + "/loveurls", 'w', encoding='utf-8') as f:
                f.truncate(0)
                print(f.write(str(loveurls)))
            with open(filepath + "/lovelrc", 'w', encoding='utf-8') as f:
                f.truncate(0)
                print(f.write(str(lovelrc)))
            with open(filepath + "/voice", 'w', encoding='utf-8') as f:
                f.truncate(0)
                print(f.write(str(voice)))
            event.accept()

        else:
            event.ignore()

    def mousePressEvent(self, event):
        global big
        big = False

        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # ��ȡ�����Դ��ڵ�λ��
            event.accept()
            # self.setCursor(QCursor(Qt.OpenHandCursor))  # �������ͼ��

    def mouseMoveEvent(self, QMouseEvent):
        global big
        big = False
        if Qt.LeftButton and self.m_flag:
            self.setWindowState(Qt.WindowNoState)
            self.move(QMouseEvent.globalPos() - self.m_Position)  # ���Ĵ���λ��
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        global big
        big = False
        self.m_flag = False
        # self.setCursor(QCursor(Qt.ArrowCursor))

    def big(self):
        global big
        print('��󻯣�{}'.format(big))
        if not big:
            self.setWindowState(Qt.WindowMaximized)
            big = True
        elif big:
            self.setWindowState(Qt.WindowNoState)
            big = False





    def mini(self):

        self.showMinimized()

    def crop_max_square(pil_img): \
            return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


def mask_circle_transparent(pil_img, blur_radius, offset=0):
    offset = blur_radius * 2 + offset
    mask = Image.new("L", pil_img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((offset, offset, pil_img.size[0] - offset, pil_img.size[1] - offset), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

    result = pil_img.copy()
    result.putalpha(mask)
    return result


def draw(lsfile, safile):
    markImg = Image.open(lsfile)
    thumb_width = 600

    im_square = crop_max_square(markImg).resize((thumb_width, thumb_width), Image.LANCZOS)
    im_thumb = mask_circle_transparent(im_square, 0)
    im_thumb.save(safile)
    remove(lsfile)


def crop_max_square(pil_img): \
        return crop_center(pil_img, min(pil_img.size), min(pil_img.size))


def get_info(url):
    print('��ʼ��ȡ����IP��ַ...')
    print('���Դ���{}'.format(tryed))
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/491.10.2623.122 Safari/537.36'
    }
    web_data = get(url, headers=headers)
    soup = BeautifulSoup(web_data.text, 'lxml')
    ranks = soup.select('#list > table > tbody > tr:nth-child({}) > td:nth-child(1)'.format(str(tryed)))
    titles = soup.select('#list > table > tbody > tr:nth-child({}) > td:nth-child(2)'.format(str(tryed)))
    times = soup.select('#list > table > tbody > tr:nth-child({}) > td:nth-child(6)'.format(str(tryed)))
    for rank, title, time in zip(ranks, titles, times):
        data = {
            'IP': rank.get_text(),
            'duan': title.get_text(),
            'time': time.get_text()
        }
        q = str('http://' + str(rank.get_text()) + '/' + str(title.get_text()))
        proxies = {
            'http': q
        }
        print('����IP��ַ��{}'.format(proxies))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()  # QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
    # app = QApplication(argv)
    # gui = Ui_MainWindow()
    # gui.setupUi(MainWindow)
    # MainWindow.show()
    # exit(app.exec_())