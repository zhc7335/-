import requests
import re

headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.9 Safari/537.36'}

#http://navi.cnki.net/knavi/JournalDetail/GetArticleList?year=2018&issue=09&pykm=GJIG&pageIdx=0&pcode=CJFD
#分析网页得到，上面为2018年9月的网址，网址内含有2018年9月所有的文章，遍历year={}和issue={}即可

#1月到12月
xl=['01','02','03','04','05','06','07','08','09','10','11','12']
#2010年到2019年
for i in range(2010,2020):
    for j in range(len(xl)):
        #构建某年某月的网址
        baseurl='http://navi.cnki.net/knavi/JournalDetail/GetArticleList?year={}&issue={}&pykm=GJIG&pageIdx=0&pcode=CJFD'.format(i,xl[j])
        print(baseurl)
        #获取某年某月的网页内容
        basedata=requests.get(baseurl,headers=headers)
        basedata=basedata.text
        #分析每一篇文章的网页，http://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename=GJIG201809001&dbname=CJFDLAST2018
        #发现每一篇文章的网址只有filename={}和dbname={}在改变，所以只有抓取取filename和dbname就可以构造每一篇文章的网址
        filename=re.findall(r'amp;filename=(.*?)&amp;tableName',basedata)
        tablename=re.findall(r'tableName=(.*?)&amp;url=',basedata)
        for m in range(len(filename)):
            #构造每一篇文章的网址
            detailurl='http://kns.cnki.net/kcms/detail/detail.aspx?dbcode=CJFD&filename={}&dbname={}'.format(filename[m],tablename[m])
            detaildata=requests.get(detailurl,headers=headers)
            detaildata=detaildata.text
            #抓取题目
            title=re.findall(r'<h2 class="title">(.*?)</h2><a class=',detaildata)
            #抓取摘要
            zhaiyao=re.findall(r'</label><span id="ChDivSummary" name="ChDivSummary">(.*?)</span><span>',detaildata)
            print(title[0])
            #with open(f'abstract.txt','a+') as f:
                #f.write('《')
                #f.write(title[0])
                #f.write('》')
                #f.write('——')
                #f.write(zhaiyao[0])
                #f.write('\n')
            try:
                with open(f'abstract.txt','a+') as f:
                    f.write('《')
                    f.write(title[0])
                    f.write('》')
                    f.write('——')
                    f.write(zhaiyao[0])
                    f.write('\n')
            except Exception as e:
                print(e)
