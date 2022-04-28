import logging

import scrapy
from scrapy.http import Request

from ..items import War2022TeamZKTS84Item


class LentaRuSpider(scrapy.Spider):
    name = "lenta"
    allowed_domains = ['www.lenta.ru']
    start_url = "https://lenta.ru/rubrics/economics/economy/"

    articles_url_xpath = '//a[contains(@class,"card-full-news")]'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def start_requests(self):
        logging.info(self.start_url)
        request = Request(self.start_url, cookies={"store_language": "en"}, callback=self.parse)

        yield request

    def parse(self, response, **kwargs):
        item = War2022TeamZKTS84Item()

        article_links = response.xpath(self.articles_url_xpath)

        for link in article_links:
            item['article_url'] = "https://lenta.ru" + link.xpath('.//@href').extract_first()
            logging.info(item['article_url'])

            yield (item)
