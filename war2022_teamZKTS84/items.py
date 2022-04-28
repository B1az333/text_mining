# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class War2022TeamZKTS84Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    article_url = scrapy.Field()


class War2022TeamZKTS84Text(scrapy.Item):
    article_url = scrapy.Field()
    article_uuid = scrapy.Field()
    article_datetime = scrapy.Field()
    article_title = scrapy.Field()
    article_text = scrapy.Field()
