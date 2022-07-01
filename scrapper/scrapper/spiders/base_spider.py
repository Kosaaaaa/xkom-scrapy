import re
from datetime import datetime

import scrapy
from itemloaders.utils import arg_to_iter
from scrapy.loader import ItemLoader

from scrapper.items import ProductItem

ROOT_CATEGORY_RE = re.compile(r'/g/.+\.html')
SUBCATEGORY_RE = re.compile(r'/g-\d+/c/.+\.html')
ITEM_RE = re.compile(r'/p/.+\.html')


class CustomItemLoader(ItemLoader):
    """Item loader which allows to handle default values from DefaultValue processor."""

    def add_value(self, field_name, value, *processors, **kw):
        value = self.get_value(value, *processors, **kw)
        if not field_name:
            for k, v in value.items():
                self._add_value(k, v)
        else:
            self._add_value(field_name, value)

    def _add_value(self, field_name, value):
        value = arg_to_iter(value)
        processed_value = self._process_input_value(field_name, value)
        self._values.setdefault(field_name, [])
        self._values[field_name] += arg_to_iter(processed_value)


class BaseSpider(scrapy.Spider):
    name = 'base'
    allowed_domains = ['x-kom.pl']
    start_urls = ['https://www.x-kom.pl/']

    def parse(self, response, **kwargs):
        root_category_urls = response.css('ul.sc-1ktmy3g-2.iXwiqH a.sc-1h16fat-0.befyud-6.jnfACR::attr(href)').getall()

        for url in root_category_urls:
            if ROOT_CATEGORY_RE.match(url):
                yield response.follow(url, callback=self.parse_root_category)

    def parse_root_category(self, response, **kwargs):
        self.logger.info('This is an root category page! %s', response.url)

        subcategory_urls = response.css('li.sc-16n31g-4.fcMCVZ > ul.sc-16n31g-2.foNRTB > li > a::attr(href)').getall()

        for subcategory_url in subcategory_urls:
            if SUBCATEGORY_RE.match(subcategory_url):
                yield response.follow(subcategory_url, callback=self.parse_subcategory)

    def parse_subcategory(self, response, **kwargs):
        self.logger.info('This is an subcategory page! %s', response.url)

        next_page = response.css('a.sc-1xy3kzh-8.jpsIZh.sc-1h16fat-0.irSQpN::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse_subcategory)

        item_urls = response.xpath('//div[@id="listing-container"]') \
            .css('a.sc-1h16fat-0.sc-1yu46qn-7.kaqYqE::attr(href)').getall()

        for item_url in item_urls:
            if ITEM_RE.match(item_url):
                yield response.follow(item_url, callback=self.parse_item)

    def parse_item(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)

        item_loader = ItemLoader(item=ProductItem(), selector=response)

        item_loader.add_value('link', response.url)
        item_loader.add_css('short_specification', 'div.sc-14h089p-0.kLcxHK.sc-eqIVtm.elwVVk > ul > li')
        item_loader.add_css('name', 'h1::text')
        item_loader.add_value('test', None)
        item_loader.add_value('last_updated', datetime.now().isoformat())
        item_loader.add_css('price', 'div.n4n86h-4.eKNYud')

        yield item_loader.load_item()
