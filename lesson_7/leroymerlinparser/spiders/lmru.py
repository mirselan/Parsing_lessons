import scrapy
from scrapy.http import HtmlResponse
from leroymerlinparser.items import LeroymerlinparserItem
from scrapy.loader import ItemLoader


class LmruSpider(scrapy.Spider):
    name = 'lmru'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        super().__init__()
        self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']

    def parse(self, response: HtmlResponse):
        ads_links = response.xpath("//a[@data-qa='product-name']")
        next_page = response.xpath("//a[@data-qa-pagination-item='right']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        for link in ads_links:
            yield response.follow(link, callback=self.ads_parse)

    def ads_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroymerlinparserItem(), response=response)
        loader.add_value('url', response.url)
        loader.add_xpath('name', "//h1/text()")
        loader.add_xpath('params', "//section[@id='nav-description']/descendant::p[2]/text()")
        loader.add_xpath('price', "////span[@slot='price']/text()")
        loader.add_xpath('photos', "//img[@alt='product image']/@src")

        yield loader.load_item()
