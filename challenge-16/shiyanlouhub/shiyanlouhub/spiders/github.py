# -*- coding: utf-8 -*-
import scrapy
from shiyanlouhub.items import RepositoriesItem


class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['https://github.com/']

    @property
    def start_urls(self):
        yield ('https://github.com/shiyanlou?page={}&tab=repositories'.format(i) for i in range(0, 5))

    def parse(self, response):
        for item in response.xpath('//*[@id="user-repositories-list"]//li[@class="source"]'):
            yield RepositoriesItem({
                'name': item.xpath('.//h3/a/text()').extract_first(),
                'update_time': item.xpath('.//relative-time/@datetime').extract_first()
            })
