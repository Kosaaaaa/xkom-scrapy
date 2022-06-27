"""
playwright based spider - clone of BaseSpider
"""
from datetime import datetime

import scrapy
from itemloaders.processors import MapCompose
from scrapy.loader import ItemLoader
from scrapy_playwright.page import PageMethod

from scrapper.items import ProductItem


class PwBaseSpider(scrapy.Spider):
    name = 'pw_base'

    start_urls = [
        'https://www.x-kom.pl/g-5/c/11-procesory.html',
        'https://www.x-kom.pl/g-5/c/345-karty-graficzne.html',
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, meta={
                'playwright': True,
                'playwright_include_page': True,
                'playwright_page_coroutines': [
                    PageMethod('wait_for_selector', 'div#listing-container'),
                ],
            })

    async def parse(self, response, **kwargs):
        for products in response.xpath('//div[@id="listing-container"]'):
            for product in products.css('div.sc-162ysh3-1.dAqvUz.sc-eqIVtm.ejDbRM'):
                item_loader = ItemLoader(item=ProductItem(), selector=product)

                item_loader.add_css('name', 'h3.sc-1yu46qn-9.hpBlAC.sc-16zrtke-0.fafaJG::attr("title")')
                item_loader.add_css('link', 'a.sc-1h16fat-0.irSQpN::attr("href")', MapCompose(response.urljoin))
                item_loader.add_css('price', 'span.sc-6n68ef-0.sc-6n68ef-3.iepkXv')
                item_loader.add_css('old_price', 'span.sc-6n68ef-0.sc-6n68ef-2.iekuDC')
                item_loader.add_value('last_updated', datetime.now().isoformat())

                yield item_loader.load_item()

        next_page = response.css('a.sc-1xy3kzh-8.jpsIZh.sc-1h16fat-0.irSQpN::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
