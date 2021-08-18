# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BooksSpider(CrawlSpider):
    name = 'books_scraper'
    allowed_domains = ['books.toscrape.com']

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='http://books.toscrape.com/', headers={
            'User-Agent': self.user_agent
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//*[@id="default"]/div/div/div/div/section/div[2]/ol/li/article/h3/a'), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths='//*[@id="default"]/div/div/div/div/section/div[2]/div/ul/li/a'), process_request='set_user_agent')
    )

    def set_user_agent(self, request, response):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        yield {
            'title': response.xpath('//*[@id="content_inner"]/article/div[1]/div[2]/h1/text()').get(),
            'price': response.xpath('//*[@id="content_inner"]/article/div[1]/div[2]/p[1]/text()').get(),
        }