import requests
import re

#1、分析目标网页，确定爬取的url路径，headers参数
base_url='https://game.gtimg.cn/images/lol/act/img/js/heroList/hero_list.js'
headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.9 Safari/537.36'}

#2、发送请求
response=requests.get(base_url,headers=headers)
#response.encoding = 'utf-8'
base_data=response.json()
base_data=str(base_data)

#3、抓取数据并储存
data_id=re.findall(r"heroId': '(.*?)', 'name",base_data)
for i in range(len(data_id)):
               item=data_id[i]
               #print(item)
               hero_url='https://game.gtimg.cn/images/lol/act/img/js/hero/{}.js'.format(item)
               #print(hero_url)
               response_hero=requests.get(hero_url,headers=headers)
               data_hero_detail=response_hero.json()
               #print(data_hero_detail)
               data_hero_detail=str(data_hero_detail)
               skin_url=re.findall(r"mainImg': '(.*?)', 'iconImg",data_hero_detail)
               #print(skin_url)
               #data_hero_detail=str(data_hero_detail)
               skin_id=re.findall(r"skinId': '(.*?)', 'heroId",data_hero_detail)
               skin_name=re.findall(r"heroName': '(.*?)', 'heroTitle",data_hero_detail)
               #print(skin_id,skin_name)
               for skin_num in range(len(skin_url)):
                    skin_no=skin_url[skin_num]
                    try:
                        skin_img=requests.get(skin_no,headers=headers).content
                        with open('LOL_SKIN\\'+skin_name[skin_num]+'-'+skin_id[skin_num]+'.jpg','wb') as f:
                                print('正在下载图片:',skin_name[skin_num]+'-'+str(skin_id[skin_num]))
                                f.write(skin_img)
                    except Exception as e:
                        print(e)
