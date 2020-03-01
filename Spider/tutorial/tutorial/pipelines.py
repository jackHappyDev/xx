# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class TutorialPipeline(object):
    def open_spider(self, spider):
        self.fo = open('doubantop250.txt', 'a')

    def process_item(self, item, spider):
        data = "{}\n****************************************************************************\n".format(item['huilv'])
        self.fo.write(data)
        return item

    def close_spider(self, spider):
        self.fo.close()