# -*- coding: utf-8 -*-
import scrapy
from shiyanlouhub.items import RepositoryItem

class RepositorySpider(scrapy.Spider):
    name = 'repository'
    @property
    def start_urls(self):
        url_tmpl='https://github.com/shiyanlou?page={}&tab=repositories'
        for i in range(1,5):
            yield url_tmpl.format(i)

    def parse(self, response):
        for item_selector in response.xpath('//li[@itemprop="owns"]'):
            item = RepositoryItem({
                    'name': item_selector.xpath('.//h3/a/text()').re_first('\s*(\S+)\s*'),
                    'update_time': item_selector.xpath('.//relative-time/@datetime').extract_first(),
                })
            url = item_selector.xpath('.//h3/a/@href').extract_first()
            request = response.follow(url,callback=self.more_info_parse)
            request.meta['item'] = item
            yield request

    def more_info_parse(self,response):
        item = response.meta['item']
        item['commits']=response.xpath('//ul[@class="numbers-summary"]/li[1]//span/text()').extract_first().strip()

        item['branches']=response.xpath('//ul[@class="numbers-summary"]/li[2]//span/text()').extract_first().strip()
        item['releases']=response.xpath('//ul[@class="numbers-summary"]/li[3]//span/text()').extract_first().strip()
        yield item
