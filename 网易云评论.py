from selenium import webdriver
import time

class yunspider(object):
    # 初始化方法
    def __init__(self,url):
        self.url=url
        # 打开浏览器
        self.driver=webdriver.Chrome()

    # 打开网站 提取数据 翻页
    def getcountent(self):
        # 打开网址
        self.driver.get(self.url)
        # 写js，让页面滚动条滑到底,先进入IFrame
        self.driver.switch_to.frame(0) #0代表第一个框
        js='window.scrollBy(0,8000)'
        self.driver.execute_script(js)

        # 翻页
        for page in range(99):
            selectors=self.driver.find_elements_by_xpath('//div[@class="cmmts j-flag"]/div')
            for selector in selectors:
                text=selector.find_element_by_xpath('.//div[@class="cnt f-brk"]').text
                #print(text)
                #调用存储数据的功能 两种方法
                #self.savedata(text)
                yunspider.savedata(text)
                print('写入一页')

            # 找到“下一页”的元素 然后进行点击
            # find_element_by_partial_link_text 获取文本链接
            nextpage=self.driver.find_element_by_partial_link_text('下一页')
            # 点击下一页
            nextpage.click()
            time.sleep(1)

    # 保存数据
    @staticmethod
    def savedata(item):
        with open('yuncountent.txt','a',encoding='utf-8') as f:
            f.write(item+'\n')


if __name__=='__main__':
    url='https://music.163.com/#/song?id=1442031605'
    yunspider=yunspider(url)
    yunspider.getcountent()