#北京交通大学经济管理学院老师信息，并导入本地数据库

import requests
import re
import pymysql

db = pymysql.connect('localhost','root','126315','petzhang')
cursor = db.cursor()

for i in range(1,40):
    baseurl = 'http://sem.bjtu.edu.cn/lists-szjs.html?szyx=0&leixing=0&zhicheng=0&zimu=&k=&page={}'.format(i)
    headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.9 Safari/537.36'}
    basedata = requests.get(baseurl, headers=headers).text
    teacher_data = re.findall(r'<a class="bw_a" href="(.*?)">',basedata)
    for j in range(len(teacher_data)):
        teacher_url = 'http://sem.bjtu.edu.cn{}'.format(teacher_data[j])
        detail_data = requests.get(teacher_url, headers=headers).text
        teacher_name = re.findall(r'<h6>(.*?)</h6><br />',detail_data)
        teacher_loca = re.findall(r'<span>办公地点:</span><span>(.*?)</span></p>', detail_data)
        if len(teacher_loca)==0:
            teacher_loca=['/']
        teacher_zhicheng = re.findall(r'<span>教师职称:</span><span>(.*?)</span></p>', detail_data)
        if len(teacher_zhicheng)==0:
            teacher_zhicheng=['/']
        teacher_leixing = re.findall(r'<span>导师类型:</span><span>(.*?)</span></p>', detail_data)
        if len(teacher_leixing)==0:
            teacher_leixing=['/']
        teacher_xi = re.findall(r'<span>所属系 :</span><span>(.*?)</span></p>', detail_data)
        if len(teacher_xi)==0:
            teacher_xi=['/']
        teacher_mail = re.findall(r'<span>邮箱:</span><span>(.*?)</span></p>', detail_data)
        if len(teacher_mail)==0:
            teacher_mail=['/']
        teacher_lingyu = re.findall(r'<p><p>(.*?)</p></p>', detail_data)
        if len(teacher_lingyu)==0:
            teacher_lingyu=['/']
        try:
            sql = 'insert into `teacher` (`姓名`,`办公地点`,`教师职称`,`导师类型`,`所属系`,`邮箱`,`研究领域`) values ("{}","{}","{}","{}","{}","{}","{}")'.format(teacher_name[0],teacher_loca[0],teacher_zhicheng[0],teacher_leixing[0],teacher_xi[0],teacher_mail[0],teacher_lingyu[0])
            cursor.execute(sql)
            db.commit()
            print("已存储"+teacher_name[0])
        except Exception as e:
            print(e)