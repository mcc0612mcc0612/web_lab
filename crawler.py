#coding=utf-8
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re
import unicodedata
from csv import DictWriter
options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')   #主要是该条
options.add_argument('--ignore-ssl-errors')
class DoubanParser:
    driver = webdriver.Chrome()
    records = []
    def parse(self,page_url): 
        self.driver.get(page_url)
        html = self.driver.page_source
        page_soup = BeautifulSoup(html,features='lxml')
        movie_titles = page_soup.find('div',{'id':'content'})
        title = movie_titles.h1.select('span')[0].string##title : content > h1 > span:nth-child(1)
        year = movie_titles.h1.select('span')[1].string#
        year = year.replace('(','')
        year = year.replace(')','')
        print (year)
        movie_summary = page_soup.find('div',{'id':'link-report'})
        summary = movie_summary.span.get_text()##summary:#link-report > span
        #summary = ''.join(summary.split())##剔除空格与换行符
        summary = summary.replace("\u3000",'')
        summary = summary.replace(' ','')
        movie_dict = {'movie':title,'year':year,'link':page_url,'summary':summary}
        movie_cast = page_soup.find_all('li',class_='celebrity')#celebrities > ul > li:nth-child(1)
        num_of_cel = 0
        for celebrity in movie_cast:##celebrities > ul > li:nth-child(1) > div > span.role
            num_of_cel = num_of_cel + 1
            movie_dict['celebrity'+str(num_of_cel)] = celebrity.find('span',class_='name').get_text()+' '+celebrity.find('span',class_='role').get_text()
        self.records.append(movie_dict)
    def read_txt(self):
        f = open("Movie_id.txt")
        byt = f.readlines()
        #for line in byt:
        #    url = "https://movie.douban.com/subject/"+line
        #    self.parse(url)
        self.parse("https://movie.douban.com/subject/1820156/")
        with open('douban_top_250.csv','w', newline='', encoding='utf-8-sig') as file:
            headers = [key for key in self.records[0].keys()]
            csv_writer = DictWriter(file, fieldnames=headers)
            csv_writer.writeheader()
            for record in self.records:
                csv_writer.writerow(record)
    
parser=DoubanParser()
parser.read_txt()