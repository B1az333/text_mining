import hashlib
import json
import logging

import scrapy
from scrapy.http import Request

from ..items import War2022TeamZKTS84Text


class KpRuArticlesSpider(scrapy.Spider):
    name = 'kp-articles'
    allowed_domains = ['www.kp.ru']

    def start_requests(self):
        with open('article_urls/kp.json') as json_file:
            data = json.load(json_file)

        for link_url in data:
            logging.info(f'URL:{link_url["article_url"]}')
            request = Request(link_url['article_url'], cookies={'store_language': 'ru'}, callback=self.parse)
            yield request

    def parse(self, response, **kwargs):
        item = War2022TeamZKTS84Text()
        item['article_url'] = response.url
        item['article_uuid'] = hashlib.sha256(str(response.url).encode('utf-8')).hexdigest()
        item['article_datetime'] = response.xpath('//span[contains(@class,"styled__Time")]/text()').extract()
        item['article_title'] = response.xpath('//h1[contains(@class,"styled__Heading")]/text()').extract()
        item['article_text'] = "\n".join(response.xpath('//div[contains(@class,"styled__Content")]/p/text()').extract())

        yield (item)
