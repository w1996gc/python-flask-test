import re

import parsel
import requests
from bs4 import BeautifulSoup

'''url = 'http://192.168.1.92:5756/playlisten'
requests.get(url)
text=requests.get(url).text
soup=BeautifulSoup(text,'html.parser')
content=soup.select('#content')[0].text
print(content)'''
url='https://m.bbiquge.net/book/104535/57234049.html'
hearders={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
}






