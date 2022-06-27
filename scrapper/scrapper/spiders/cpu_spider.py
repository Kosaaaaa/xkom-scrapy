from scrapper.spiders.base_spider import BaseSpider


class CpuSpider(BaseSpider):
    name = 'cpu'
    start_urls = ['https://www.x-kom.pl/g-5/c/11-procesory.html', ]
