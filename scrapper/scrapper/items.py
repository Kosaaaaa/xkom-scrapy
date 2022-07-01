# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import re
from typing import Callable, Union, TypeVar, AnyStr

import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags

Numeric = TypeVar('Numeric')


def remove_currency(text: str) -> float:
    """Parse str representation of price to float
        123,00 zł -> 123.0
    """
    return float(re.sub(r'\D', '', text)) / 100


class DefaultValue:
    def __init__(self, default: Union[Callable, Numeric, AnyStr]) -> None:
        self.default = default

    def __call__(self, values):
        if values is not None:
            return values
        if callable(self.default):
            return self.default()
        return self.default


class ProductItem(scrapy.Item):
    name = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    short_specification = scrapy.Field(input_processor=MapCompose(remove_tags))
    test = scrapy.Field(input_processor=DefaultValue(list))
    last_updated = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(remove_tags, remove_currency), output_processor=TakeFirst())
