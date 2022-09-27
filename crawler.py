#coding=utf-8
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import unicodedata
from csv import DictWriter
import os
import requests
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')   #主要是该条
options.add_argument('--ignore-ssl-errors')
chromeOptions = webdriver.ChromeOptions()
class DoubanParser:
    driver = webdriver.Chrome()
    records = []
    '''def header_x():
    # 随机获取一个headers
        user_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
                      'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
                      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2',
                      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
                      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER',
                      'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0'
                      ]

        headers = {
        "User-Agent": random.choice(user_agents)
        }
        return headers'''
    def get_proxy(Any):
        return requests.get("http://127.0.0.1:5010/get/").json()

    def delete_proxy(proxy,Any):
        requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

# your spider code

    def getHtml(self,url):
    # ....
        retry_count = 5
        proxy = self.get_proxy().get("proxy")
        chromeOptions.add_argument("--proxy-server=http://"+proxy)
        browser = webdriver.Chrome(chrome_options = chromeOptions)
        while retry_count > 0:
            try:
                self.driver.get(url)
                # 使用代理访问
                html = self.driver.page_source
                return html
            except Exception:
                retry_count -= 1
        # 删除代理池中代理
        self.delete_proxy(proxy)
        return None

    def parse(self,page_url): 
        #headers = self.header_x()
        #self.driver.get(page_url,headers=headers)
        #html = self.driver.page_source
        try:
            html = self.getHtml(page_url)
            while(html == None):
                html = self.getHtml(page_url)
            page_soup = BeautifulSoup(html,features='lxml')
            movie_titles = page_soup.find('div',{'id':'content'})
            title = movie_titles.h1.select('span')[0].string##title : content > h1 > span:nth-child(1)
            year = movie_titles.h1.select('span')[1].string#
            year = year.replace('(','')
            year = year.replace(')','')
            movie_summary = page_soup.find('div',{'id':'link-report'})
            summary = movie_summary.span.get_text()##summary:#link-report > span
            #summary = ''.join(summary.split())##剔除空格与换行符
            summary = summary.replace("\u3000",'')
            summary = summary.replace(' ','')
            summary = summary.replace('\n','')
            movie_dict = {'movie':title,'year':year,'link':page_url,'summary':summary}
            movie_cast = page_soup.find_all('li',class_='celebrity')#celebrities > ul > li:nth-child(1)
            num_of_cel = 0
            for celebrity in movie_cast:##celebrities > ul > li:nth-child(1) > div > span.role
                num_of_cel = num_of_cel + 1
                movie_dict['celebrity'+str(num_of_cel)] = celebrity.find('span',class_='name').get_text()+' '+celebrity.find('span',class_='role').get_text()
            self.records.append(movie_dict)
        except:
            print("page:"+page_url+"doesn't exist")
    def read_txt(self):
        num = 1
        f = open("Movie_id.txt")
        byt = f.readlines()
        for line in byt:
            url = "https://movie.douban.com/subject/"+line
            self.parse(url)
            print(num,"has been resolved")
            num =num + 1
        '''url = "https://movie.douban.com/subject/1309046/";
        self.parse(url)
        url = "https://movie.douban.com/subject/1418192/";
        self.parse(url)'''
        if os.path.exists("douban_top_250.csv"):
            os.remove("douban_top_250.csv")
        with open('douban_top_250.csv','w', newline='', encoding='utf-8-sig') as file:
            headers = [key for key in self.records[0].keys()]
            csv_writer = DictWriter(file, fieldnames=headers)
            csv_writer.writeheader()
            for record in self.records:
                csv_writer.writerow(record)
    
parser=DoubanParser()
parser.read_txt()