import hashlib
import json
import logging

import scrapy
from scrapy.http import Request

from ..items import War2022TeamZKTS84Text


class PravdaOrgArticlesSpider(scrapy.Spider):
    name = 'pravda-articles'
    allowed_domains = ['www.epravda.com.ua']

    def start_requests(self):
        with open('article_urls/pravda.json') as json_file:
            data = json.load(json_file)

        for link_url in data:
            logging.info(f'URL:{link_url["article_url"]}')
            request = Request(link_url['article_url'], cookies={'store_language': 'ru'}, callback=self.parse)
            yield request

    def parse(self, response, **kwargs):
        item = War2022TeamZKTS84Text()
        item['article_url'] = response.url
        item['article_uuid'] = hashlib.sha256(str(response.url).encode('utf-8')).hexdigest()
        item['article_datetime'] = response.xpath('//div[@class="post__time"]/text()').extract()
        item['article_title'] = response.xpath('//h1[@class="post__title"]/text()').extract()
        item['article_text'] = "\n".join(response.xpath('//div[@class="post__text"]/p/span/text()').extract())

        yield (item)
