import logging

import scrapy
from scrapy.http import Request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

from ..items import War2022TeamZKTS84Item


class SvobodaOrgSpider(scrapy.Spider):
    name = "svoboda"
    allowed_domains = ['www.svoboda.org']
    start_url = "https://www.svoboda.org/z/16553"

    next_page_button_xpath = '//a[contains(@class, "link-showMore")]'
    article_url_xpath = '//div[contains(@class, "media-block__content")]/a'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.driver = webdriver.Chrome(ChromeDriverManager().install())

    def start_requests(self):
        self.driver.get(self.start_url)
        logging.info(self.start_url)

        for _ in range(8):
            current_url = self.driver.current_url
            request = Request(current_url, cookies={"store_language": "en"}, callback=self.parse)

            wait = WebDriverWait(self.driver, 30)
            wait.until(EC.element_to_be_clickable((By.XPATH, self.next_page_button_xpath)))

            load_more_button = self.driver.find_element(By.XPATH, self.next_page_button_xpath)

            for _ in range(4):
                ActionChains(self.driver).move_to_element(load_more_button).perform()
                load_more_button.click()

            yield request

    def parse(self, response, **kwargs):
        item = War2022TeamZKTS84Item()

        article_links = response.xpath(self.article_url_xpath)

        for link in article_links:
            item['article_url'] = "https://www.svoboda.org" + link.xpath('.//@href').extract_first()
            logging.info(item['article_url'])

            yield (item)
