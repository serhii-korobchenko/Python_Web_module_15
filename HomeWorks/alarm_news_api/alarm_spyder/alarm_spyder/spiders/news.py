import scrapy
from bs4 import BeautifulSoup
import re
#from ..items import ManualScrapingItem
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from scrapy.selector import Selector
from scrapy_selenium import SeleniumRequest


class NewsSpider(scrapy.Spider):
    name = 'news'

    # start custom settings
    custom_settings = {

        # 'ITEM_PIPELINES': {
        # 'serhii_spyder_bot.pipelines.SerhiiSpyderBotPipeline': 300
        #                    },

        "FEEDS": {
            'news_info.json': {
                'format': 'jsonlines',
                'encoding': 'utf8',
                'overwrite': True,

            },
        },

        "SPIDER_MIDDLEWARES": {
            'alarm_spyder.middlewares.NewsSpyderMiddleware': 548,
        }
    }
    # stop custom settings


    # allowed_domains = ['unian.ua']
    start_urls = ['https://www.unian.ua/tag/kijiv']

    def __init__(self):
        self.driver = webdriver.Chrome(executable_path="chromedriver.exe")

    def parse(self, response):

        self.driver.get(response.url)
        time.sleep(10)
        new_height = self.driver.execute_script("return document.body.scrollHeight")  # initialize new_neight first
        flag = 0
        outer = 0
        while True:
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(10)

            prev_height = new_height  # update prev_height
            flag +=1
            outer +=1
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == prev_height or flag == 2:
                break

        scrapy_selector = Selector(text=self.driver.page_source)


        for item in range(1, 61):
            yield {
                "news_title": scrapy_selector.xpath(f'//*[@id="block_left_column_content"]/div/div/div/h3/a[@class="list-thumbs__title"]/text()').extract(),
                "date_time": scrapy_selector.xpath(f'//*[@id="block_left_column_content"]/div/div/div/div/text()').extract()

                       }
        # for item in range(1, 21):
        #     yield {
        #         "news_title": scrapy_selector.xpath(f'//*[@id="block_left_column_content"]/div[2]/div[{item}]/div/h3/a[@class="list-thumbs__title"]/text()').extract(),
        #         "date_time": scrapy_selector.xpath(f'//*[@id="block_left_column_content"]/div[2]/div[{item}]/div/div/text()').extract()
        #           }
