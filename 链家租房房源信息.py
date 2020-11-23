# 安居客北京市租房信息，并导入本地数据库

import requests
import re
import pymysql

db = pymysql.connect('localhost', 'root', '636458', 'petzhang')
cursor = db.cursor()
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.9 Safari/537.36'}


def getdata(n):
    first_url = 'https://bj.lianjia.com/zufang/chaoyang/pg{}'.format(n)
    response = requests.get(first_url, headers=headers)
    # print(response.text)

    # 市区（朝阳、海淀等等）
    loc_data1 = re.findall(r'<a target="_blank" href="/zufang/(.*?)/a>-<a href="/zufang/', response.text)
    loca1 = []
    for m in range(len(loc_data1)):
        locdata1 = re.findall(r'[\u4e00-\u9fa5]+', loc_data1[m])
        locdata1 = ''.join(locdata1)
        loca1.append((locdata1))

    # 应该是办事处吧
    loca2 = re.findall(r'target="_blank">(.*?)</a>-<a title=', response.text)

    # 应该是小区
    loca3 = re.findall(r'</a>-<a title="(.*?)" href=', response.text)

    detail_url = re.findall(r'<a target="_blank" href="/zufang/BJ(.*?)">', response.text)
    # print(detail_url)
    url1 = []
    title1 = []
    price1=[]
    method1=[]
    leixing1=[]
    square1=[]
    chaoxiang1=[]
    ruzhushijian1=[]
    louceng1=[]
    dianti1=[]
    yongshui1=[]
    yongdian1=[]
    ranqi1=[]
    cainuan1=[]
    zuqi1=[]
    agent1=[]
    phone1=[]
    for i in range(len(detail_url)):
        detailurl = 'https://bj.lianjia.com/zufang/BJ{}'.format(detail_url[i])
        detail_data = requests.get(detailurl, headers=headers)
        #网址
        url = detailurl
        url1.append(url)
        #房源标题
        title = re.findall(r'<p class="content__title">(.*?)</p>', detail_data.text)
        title1.append(title)
        #价格
        price=re.findall(r'<span>(.*?)</span>元/月', detail_data.text)
        price1.append(price)
        #租赁方式
        method = re.findall(r'<li><span class="label">租赁方式：</span>(.*?)</li>', detail_data.text)
        method1.append(method)
        #房屋类型
        leixing = re.findall(r'<li><span class="label">房屋类型：</span>(.*?)</li>', detail_data.text)
        leixing1.append(leixing)
        #面积
        square = re.findall(r'<li class="fl oneline">面积：(.*?)</li>', detail_data.text)
        square1.append(square)
        #朝向
        chaoxiang = re.findall(r'<li class="fl oneline">朝向：(.*?)</li>', detail_data.text)
        chaoxiang1.append(chaoxiang)
        #入住
        ruzhushijian = re.findall(r'<li class="fl oneline">入住：(.*?)</li>', detail_data.text)
        ruzhushijian1.append(ruzhushijian)
        #楼层
        louceng = re.findall(r'<li class="fl oneline">楼层：(.*?)</li>', detail_data.text)
        louceng1.append(louceng)
        #电梯
        dianti = re.findall(r'<li class="fl oneline">电梯：(.*?)</li>', detail_data.text)
        dianti1.append(dianti)
        #用水
        yongshui = re.findall(r'<li class="fl oneline">用水：(.*?)</li>', detail_data.text)
        yongshui1.append(yongshui)
        #用电
        yongdian = re.findall(r'<li class="fl oneline">用电：(.*?)</li>', detail_data.text)
        yongdian1.append(yongdian)
        #燃气
        ranqi = re.findall(r'<li class="fl oneline">燃气：(.*?)</li>', detail_data.text)
        ranqi1.append(ranqi)
        #采暖
        cainuan = re.findall(r'<li class="fl oneline">采暖：(.*?)</li>', detail_data.text)
        cainuan1.append(cainuan)
        #租期
        zuqi = re.findall(r'<li class="fl oneline">租期：(.*?)</li>', detail_data.text)
        zuqi1.append(zuqi)
        #代理人
        agent = re.findall(r'name":"(.*?)","office', detail_data.text)
        agent1.append(agent)
        #代理人联系方式
        phone = re.findall(r'phone400":"(.*?)","phone', detail_data.text)
        phone1.append(phone)
    print('page'+'-'+str(n))

    try:
        for j in range(len(title1)):
            #print(title1[j][0])
            sql = 'insert into `chaoyang` (`房源标题`,`网址`,`市区`,`商圈`,`小区`,`租赁方式`,`价格`,`房屋类型`,`面积`,`朝向`,`入住`,`楼层`,`电梯`,`用水`,`用电`,`燃气`,`采暖`,`租期`,`代理人`,`联系方式`) values ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'\
                .format(title1[j][0], url1[j], loca1[j], loca2[j], loca3[j], method1[j][0],
                        price1[j][0], leixing1[j][0], square1[j][0], chaoxiang1[j], ruzhushijian1[j][0],
                        louceng1[j][0], dianti1[j][0], yongshui1[j][0], yongdian1[j][0], ranqi1[j][0],
                        cainuan1[j][0], zuqi1[j][0], agent1[j][0], phone1[j][0])
            cursor.execute(sql)
            db.commit()
            print("已存储" + title1[j][0])
    except Exception as e:
        print(e)

'''
def savedata():
    try:
        for j in range(len(title1)):
            # print(title1[j][0])
            sql = 'insert into `chaoyang` (`房源标题`,`网址`,`市区`,`商圈`,`小区`,`租赁方式`,`价格`,`房屋类型`,`面积`,`朝向`,`入住`,`楼层`,`电梯`,`用水`,`用电`,`燃气`,`采暖`,`租期`,`代理人`,`联系方式`) values ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")' \
                .format(title1[j][0], url1[j], loca1[j], loca2[j], loca3[j], method1[j][0],
                        price1[j][0], leixing1[j][0], square1[j][0], chaoxiang1[j], ruzhushijian1[j][0],
                        louceng1[j][0], dianti1[j][0], yongshui1[j][0], yongdian1[j][0], ranqi1[j][0],
                        cainuan1[j][0], zuqi1[j][0], agent1[j][0], phone1[j][0])
            cursor.execute(sql)
            db.commit()
            print("已存储" + title1[j][0])
    except Exception as e:
        print(e)
'''
if __name__ == '__main__':
    for n in range(1,101):
        getdata(n)

