import csv
import asyncio
import aiohttp
import async_timeout
from  scrapy.http import HtmlResponse

results = []

async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()


def parse(url,body):
    response = HtmlResponse(url=url,body=body,encoding='utf-8')
    for item in response.xpath('//li[@itemprop="owns"]'):
        name = item.xpath('.//h3//a/text()').extract_first().strip()
        updatetime = item.xpath('.//relative-time/@datetime').extract_first()
        results.append((name,updatetime))

async def task(url):
    async with aiohttp.ClientSession() as session:
        body = await fetch(session, url)
        parse(url,body)

def main():
    loop = asyncio.get_event_loop()
    url_template = 'https://github.com/shiyanlou?page={}&tab=repositories'
    tasks = [task(url_template.format(i)) for i in range(1, 5)]
    loop.run_until_complete(asyncio.wait(tasks))
    with open('/home/shiyanlou/shiyanlou-repos.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(results)

if __name__ == '__main__':
    main()
        
