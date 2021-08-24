# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    old_price = scrapy.Field()
    new_price = scrapy.Field()
    rating = scrapy.Field()
    authors = scrapy.Field()
    books_link = scrapy.Field()
    pass
