import scrapy


class GitHubSpider(scrapy.Spider):

    name = 'GitHub Spider'

    @property
    def start_urls(self):
        tmpl_url = 'https://github.com/shiyanlou?page={}&tab=repositories'
        for i in range(1, 5):
            yield tmpl_url.format(i)

    def parse(self, rsp):
        for item in rsp.xpath('//*[@id="user-repositories-list"]/ul/li'):
            yield {
                'name': item.xpath('./div[1]/h3/a/text()').re_first(r'\s*(\w+)\s*'),
                'update_time': item.xpath('.//relative-time/@datetime').extract_first()
            }
