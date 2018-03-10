# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from flask_doc.items import PageItem
import re

class FlaskSpider(scrapy.spiders.CrawlSpider):
    name = 'flask'
    start_urls = ['http://flask.pocoo.org/docs/0.12/']

    rules=[
        Rule(LinkExtractor(restrict_xpaths='//a[@class="reference internal"]'), callback='parse_page', follow=False),
    ]

    def parse_page(self, response):
        yield PageItem({
            'url': response.url,
            'text': re.sub(r'<.*?>','',response.xpath('//div[@role="main"]').extract_first())
        })
