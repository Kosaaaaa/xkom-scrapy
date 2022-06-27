from scrapper.spiders.base_spider import BaseSpider


class GpuSpider(BaseSpider):
    name = 'gpu'
    start_urls = ['https://www.x-kom.pl/g-5/c/345-karty-graficzne.html']
