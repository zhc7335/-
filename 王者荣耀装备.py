#爬取王者荣耀装备，并写入MySQL数据库

import requests
import re
import pymysql

db=pymysql.connect('localhost','root','126315','petzhang')
cursor=db.cursor()

#1、分析目标网页，确定爬取的url路径，headers参数
    #王者荣耀官网内有如下网址存储着装备列表，所以直接抓取下面的网址就可以
url='http://pvp.qq.com/web201605/js/item.json'

#2、发送请求
response=requests.get(url)
response=response.json()
#print(type(response))

#3、存取数据
for i in  range(len(response)):
    item = response[i]
    sql1='insert into `equip` (`item_id`,`item_name`,`item_type`,`price`,`total_price`) values ("{}","{}","{}","{}","{}")'
    sql1=sql1.format(item['item_id'],item['item_name'],item['item_type'],item['price'],item['total_price'])
    cursor.execute(sql1)
    db.commit()
