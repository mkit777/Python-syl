# -*- coding: utf-8 -*-
import scrapy
from shiyanlouhub.items import RepositoriesItem


class GithubSpider(scrapy.Spider):
    name = 'github'

    @property
    def start_urls(self):
        return ('https://github.com/shiyanlou?page={}&tab=repositories'.format(i) for i in range(1, 5))

    def parse(self, response):
        for item in response.xpath('//*[@id="user-repositories-list"]//li[@itemprop="owns"]'):
            yield RepositoriesItem({
                'name': item.xpath('.//h3/a/text()').extract_first().strip(),
                'update_time': item.xpath('.//relative-time/@datetime').extract_first()
            })
