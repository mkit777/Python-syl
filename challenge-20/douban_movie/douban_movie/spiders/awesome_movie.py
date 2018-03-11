# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor
from douban_movie.items import MovieItem
from douban_movie.pipelines import DoubanMoviePipeline
class AwesomeMovieSpider(CrawlSpider):
    name = 'awesome-movie'
    start_urls = ['http://movie.douban.com/subject/3011091/']
    rules=(
        Rule(LinkExtractor(restrict_xpaths='//div[@id="recommendations"]'),
            follow = True,
            callback = 'parse_movie_page'
            ),
    )


    def parse_movie_page(self, response):
        if DoubanMoviePipeline.count>40:
            return
        yield MovieItem({
            'url': response.url,
            'name':response.xpath('//h1/span[1]/text()').extract_first(),
            'summary':response.xpath('//div[@id="link-report"]/span[1]/text()').extract_first(),
            'score': response.xpath('//strong[contains(@class,"rating_num")]/text()').extract_first(),
        })

