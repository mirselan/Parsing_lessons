import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/genres/2304/']

    def parse(self, response: HtmlResponse):
        links = response.xpath("//a[@class='cover']/@href").extract()
        next_page = response.xpath("//a[@class='pagination-next__text']/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        for link in links:
            yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        name_data = response.xpath("//h1/text()").extract_first()
        old_price_data = response.xpath("//span[@class='buying-priceold-val-number']/text()").extract_first()
        new_price_data = response.xpath("//span[@class='buying-pricenew-val-number']/text()").extract_first()
        rating_data = response.xpath("//div[@id='rate']/text()").extract_first()
        link_data = response.xpath("//meta[@property='og:url']/@content").extract_first()
        authors_data = response.xpath("//div[@class='authors']//a/text()").extract()
        yield BookparserItem(name=name_data, old_price=old_price_data,
                             new_price=new_price_data, rating=rating_data,
                             authors=authors_data, books_link=link_data)
