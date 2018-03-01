# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
from shiyanlouhub.models import engine, Repositories
from sqlalchemy.orm import sessionmaker


class ShiyanlouhubPipeline(object):
    def process_item(self, item, spider):
        item['update_time'] = datetime.strptime(
            item['update_time'], '%Y-%m-%dT%H:%M:%SZ')
        self.session.add(Repositories(**item))
        return item

    def open_spider(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def cloase_spider(self):
        self.session.commit()
        self.session.close()
