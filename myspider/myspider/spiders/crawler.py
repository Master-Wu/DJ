# -*- coding: utf-8 -*-
import scrapy


class CrawlerSpider(scrapy.Spider):
    name = 'crawler'
    allowed_domains = ['flightaware.com']
    start_urls = ['http://flightaware.com/']

    def parse(self, response):
        pass
