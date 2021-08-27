# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
from itemloaders.processors import MapCompose, TakeFirst
import scrapy


def get_price(value):
    if ' ' in value:
        value = value.replace(' ', '')
    try:
        return int(value)
    except:
        return value


class LeroymerlinparserItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field(output_processor=TakeFirst())
    params = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    price = scrapy.Field(input_processor=MapCompose(get_price), output_processor=TakeFirst())
    url = scrapy.Field()
