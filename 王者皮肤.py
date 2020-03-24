#爬取王者荣耀全英雄皮肤

import requests
import re

#1、分析目标网页，确定爬取的url路径，headers参数
base_url='https://pvp.qq.com/web201605/js/herolist.json'
headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.9 Safari/537.36'}

#2、发送请求
response=requests.get(base_url,headers=headers)
base_data=response.json()
#print(base_data)

#3、解析数据
for data in base_data:
    #print(data)
    ename=data['ename']#英雄的编号
    cname=data['cname']#英雄的名字
    #skin_name=data['skin_name'].split('|')
    #print(ename,cname,skin_name)
    #因为在print时，到曜的时候显示报错，故取消skin_name=data['skin_name']语句
    #所以使用下面的异常捕获，try
    try:
        skin_name=data['skin_name'].split('|')#皮肤的名字使用‘|’分割,例如“正义爆轰|地狱岩魂”
    except Exception as e:
        print(e)
    #print(ename,cname,skin_name)
    #下面构建皮肤的url地址
    #range函数左闭右开
    for skin_num in range(1,len(skin_name)+1):
        skin_url='http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{}/{}-bigskin-{}.jpg'.format(ename,ename,skin_num)
        #print(skin_url)
        #获取图片，因为图片是二进制，所以需要.content来获取
        skin_data=requests.get(skin_url,headers=headers).content

#4、存取数据
        with open('skin\\'+cname+'-'+skin_name[skin_num-1]+'.jpg','wb') as f:#二进制图片使用“wb”方式写入
            print('正在下载图片:',cname+'-'+skin_name[skin_num-1])
            f.write(skin_data)