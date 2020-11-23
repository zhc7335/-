import requests
import re
import pymysql

db = pymysql.connect('localhost', 'root', '636458', 'petzhang')
cursor = db.cursor()
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36'}


def create_url():
    first_url = 'https://book.douban.com/top250'
    response = requests.get(first_url, headers=headers)
    # print(response.text)
    url = re.findall(r'<span class="thispage">1</span>(.*?)<span class="next">', response.text, re.S)
    url = re.findall(r'<a href="(.*?)" >', str(url))
    global final_url
    final_url = [first_url] + url


def get_de_url():
    create_url()
    global de_url
    de_url = []
    for url in final_url:
        response = requests.get(url, headers=headers)
        detail_url = re.findall(r'<a href="(.*?)" onclick=&#34;moreurl', response.text)
        de_url = de_url + detail_url
    # print(de_url)


def get_info():
    get_de_url()
    for url in de_url:
        print(url)


def get_infomation():
    create_url()
    for url in final_url:
        response = requests.get(url, headers=headers)
        name = re.findall(r'#34; title="(.*?)"', response.text)
        author = re.findall(r'<p class="pl">(.*?)</p>', response.text)
        score = re.findall(r'<span class="rating_nums">(.*?)</span>', response.text)
        brief = re.findall(r'<a href="https://book.douban.com/subject(.*?)</td>', response.text, re.S)
        all_brief = []
        for de_brief in brief:

            brief = re.findall(r'<span class="inq">(.*?)</span>', str(de_brief))
            if len(brief) == 0:
                brief = ['/']
            all_brief.append(brief)
        # print(all_brief)
        try:
            for j in range(len(name)):
                sql = 'insert into `book` (`name`,`author`,`score`,`brief`) values ("{}","{}","{}","{}")' \
                    .format(name[j], author[j], score[j], all_brief[j][0])
                cursor.execute(sql)
                db.commit()
                print("已存储" + name[j])
        except Exception as e:
            print(e)


if __name__ == '__main__':
    get_infomation()
