import requests
import re
import pymysql

db=pymysql.connect('localhost','root','636458','petzhang')
cursor=db.cursor()

#1、分析目标网页，确定爬取的url路径，headers参数
base_url='https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js'
headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.9 Safari/537.36'}

#2、发送请求
response=requests.get(base_url,headers=headers)
base_data=response.json()
#print(base_data)

#3、抓取数据
basedata=str(base_data)
data_id=re.findall(r"heroId': '(.*?)', 'name",basedata)
data_name=re.findall(r"name': '(.*?)', 'alias",basedata)
data_alias=re.findall(r"alias': '(.*?)', 'title",basedata)
data_title=re.findall(r"title': '(.*?)', 'roles",basedata)
data_attack=re.findall(r"attack': '(.*?)', 'defense",basedata)
data_defense=re.findall(r"defense': '(.*?)', 'magic",basedata)
data_magic=re.findall(r"magic': '(.*?)', 'difficulty",basedata)
data_difficulty=re.findall(r"difficulty': '(.*?)', 'selectAudio",basedata)
#print(data_difficulty)

#4、存取数据
for i in  range(len(data_id)):
    #print(i)
    sql1='insert into `lol_herolist` (`heroId`,`name`,`alias`,`roles`,`attack`,`defense`,`magic`,`difficulty`) values ("{}","{}","{}","{}","{}","{}","{}","{}")'
    sql1=sql1.format(data_id[i],data_name[i],data_alias[i],data_title[i],data_attack[i],data_defense[i],data_magic[i],data_difficulty[i])
    cursor.execute(sql1)
    db.commit()
