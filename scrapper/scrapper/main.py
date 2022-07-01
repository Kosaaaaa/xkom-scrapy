from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scrapper.spiders import BaseSpider


def main():
    process = CrawlerProcess(get_project_settings())

    process.crawl(BaseSpider)
    process.start()


if __name__ == '__main__':
    main()
