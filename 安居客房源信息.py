#安居客北京市租房信息，并导入本地数据库

import requests
import re
import pymysql

db = pymysql.connect('localhost','root','126315','petzhang')
cursor = db.cursor()
headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.9 Safari/537.36'}

def getdata(i):
    first_url='https://bj.zu.anjuke.com/fangyuan/p{}/'.format(i)
    response=requests.get(first_url,headers=headers)
    response.encoding = 'gzip'
    print(response.text)

if __name__ == '__main__':
    getdata(1)