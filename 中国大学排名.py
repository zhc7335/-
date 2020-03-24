#爬取中国大学2019年排名，并导入本地数据库

import requests
import re
import pymysql

db=pymysql.connect('localhost','root','126315','petzhang')
cursor=db.cursor()

#1、分析目标网页，确定爬取的url路径，headers参数
for i in range(2,3):
    #print(i)
    base_url='http://gaokao.xdf.cn/201901/10849478_{}.html'.format(i)
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.9 Safari/537.36'}
    print(base_url)

#2、发送请求
    response=requests.get(base_url,headers=headers)
    response.encoding = 'utf-8'
    data=response.text
    
    
#3、解析数据
    detail_data=re.findall(r'</colgroup>(.*?)</table>',data,re.S)[0]

    #抓取排名
    data1=re.findall(r'style="font-size:10pt;text-align:center;vertical-align:middle;height:14.28pt;width:62.27pt;">(.*?)</td>',detail_data,re.S)
    data1=''.join(data1)#转换为字符串
    #提取数字两个方法
    #法一
    data1=re.findall(r"\d+\.?\d*",data1)
    #法二
    #p=re.compile('\d+')
    #data1=p.findall(data1)
    print(data1)

    #抓取学校名称
    data2=re.findall(r'target="_blank">(.*?)</a>',detail_data,re.S)


    #抓取学校地址
    data_special=response.text.replace('\n','').replace('\t','')#去除网页源代码中的换行符、等符号
    data_detail_special=re.findall(r'</colgroup>(.*?)</table>',data_special,re.S)[0]
    data3=re.findall(r'style="font-size:10pt;text-align:center;vertical-align:middle;height:14.28pt;width:49.52pt;">(.*?)</td>',data_detail_special,re.S)
    #print(data3)
    #data3= re.sub('\n','',data3)
    #data3= re.sub('\t','',data3)

    #抓取学校评分
    data4=re.findall(r'style="font-size:10pt;text-align:center;vertical-align:middle;height:14.28pt;width:59.27pt;">(.*?)&nbsp',detail_data,re.S)
    data4=''.join(data4)
    p=re.compile('\d+\.?\d*')
    data4=p.findall(data4)
    
#4、存取数据
    print("正在写入",i)
    for t in range(len(data1)):
        #print(data1[t])
        #print(data2[t])
        sql='insert into `university` (`排名`,`学校名称`,`省市`,`评分`) values ("{}","{}","{}","{}")'.format(data1[t],data2[t],data3[t],data4[t])
        #sql="insert into `university` (`排名`,`学校名称`,`评分`) values ('{}','{}','{}')".format(data1[t],data2[t],data4[t])
        cursor.execute(sql)
        db.commit()



