# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
import redis

class FlaskDocPipeline(object):
    def process_item(self, item, spider):
        item['text']=re.sub('\s+','\n',item['text'])
        self.r.lpush('flask_doc:items',item)
        return item

    def open_spider(self,spider):
        self.r= redis.StrictRedis(host='127.0.0.1', port=6379, decode_responses=True)



