# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis
import re
from scrapy.exceptions import DropItem

class DoubanMoviePipeline(object):
    count = 0
    def open_spider(self,spider):
        self.r = redis.StrictRedis(host='localhost',port=6379,decode_responses=True)


    def process_item(self, item, spider):
        if eval(item['score']) < 8:
            raise DropItem
        temp =  item['summary']
        temp = re.sub(' ','',temp)
        item['summary']=re.sub(r'\n+',r'\n',temp)
        DoubanMoviePipeline.count+=1
        self.r.lpush('douban_movie:items',item)
        return item


