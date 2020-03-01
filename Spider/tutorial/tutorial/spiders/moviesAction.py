# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import TutorialItem
from bs4 import BeautifulSoup
class DoubanSpider(scrapy.Spider):
    name = 'moviesAction'
    allowed_domains = ['flw.ph']
    start_urls = ['http://www.flw.ph/forum-169-1.html']
    for i in range(2,31):
        str = 'http://www.flw.ph/forum-169-%d.html'% i
        print(str)
        start_urls.append(str)

    def parse(self, response):
        data = response.body
        soup = BeautifulSoup(data, "lxml")
        for x in soup.find_all('div',attrs={'class':'forumsummary'}):
            item = TutorialItem()
            print(x.string)
            item['huilv'] = x.string
            yield item



