import logging

import scrapy
from scrapy.http import Request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

from ..items import War2022TeamZKTS84Item


class PravdaComSpider(scrapy.Spider):
    name = "pravda"
    allowed_domains = ['www.epravda.com.ua']
    start_url = "https://www.epravda.com.ua/rus/search/?search=%FD%EA%EE%ED%EE%EC%E8%EA%E0%20%F0%EE%F1%F1%E8%E8"

    next_page_button_xpath = '/html/body/div[1]/div/div/ul/li[8]/a'
    article_links_xpath = '//div[contains(@class,"article__title")]/a'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def start_requests(self):
        self.driver.get(self.start_url)
        logging.info(self.start_url)

        for _ in range(8):
            current_url = self.driver.current_url
            request = Request(current_url, cookies={"store_language": "en"}, callback=self.parse)

            yield request

            wait = WebDriverWait(self.driver, 30)
            wait.until(EC.element_to_be_clickable((By.XPATH, self.next_page_button_xpath)))
            self.driver.find_element(By.XPATH, self.next_page_button_xpath).click()

    def parse(self, response, **kwargs):
        item = War2022TeamZKTS84Item()

        article_links = response.xpath(self.article_links_xpath)

        for link in article_links:
            item['article_url'] = "https://epravda.com.ua" + link.xpath('.//@href').extract_first()
            logging.info(item['article_url'])

            yield (item)
