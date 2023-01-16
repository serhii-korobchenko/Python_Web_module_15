import scrapy
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from selenium import webdriver
import time
from scrapy.selector import Selector


pages = 5  # ----->  # pages for infinite scroll
class NewsSpider(scrapy.Spider):
    name = 'news'

    # start custom settings
    custom_settings = {

        'ITEM_PIPELINES': {
        'alarm_spyder.pipelines.NewsSpyderPipeline': 400
                           },

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
        time.sleep(7)
        new_height = self.driver.execute_script("return document.body.scrollHeight")  # initialize new_neight first
        flag = 0
        outer = 0
        while True:
            self.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
            time.sleep(7)

            prev_height = new_height  # update prev_height
            flag +=1
            outer +=1
            new_height = self.driver.execute_script("return document.body.scrollHeight")

            if new_height == prev_height or flag == pages-1:  # ----->
                break

        scrapy_selector = Selector(text=self.driver.page_source)


        for _ in range(1, 20*(pages)+1):
            yield {
                "news_title": scrapy_selector.xpath(f'//*[@id="block_left_column_content"]/div/div/div/h3/a[@class="list-thumbs__title"]/text()').extract(),
                "date_time": scrapy_selector.xpath(f'//*[@id="block_left_column_content"]/div/div/div/div/text()').extract(),
                "news_ref": scrapy_selector.xpath(f"//*[@id='block_left_column_content']/div/div/div/h3/a/@href").extract()
                    }

class AirRaidAlarmsKyivSpider(scrapy.Spider):
    name = 'air_raid_alarms_kyiv'

    # start custom settings
    custom_settings = {


        'ITEM_PIPELINES': {
        'alarm_spyder.pipelines.AlarmSpyderPipeline': 300
                           },

        "FEEDS": {
            'alarm_info.json': {
                'format': 'jsonlines',
                'encoding': 'utf8',
                'overwrite': True,

            },
        },

        "SPIDER_MIDDLEWARES": {
            'alarm_spyder.middlewares.AlarmSpyderSpiderMiddleware': 543,
        }
    }
    # stop custom settings

    allowed_domains = ['kyiv.digital']
    start_urls = ['https://kyiv.digital/storage/air-alert/stats.html']
    # start_urls = ['file:///D:/Test/view-source_https___kyiv.digital_storage_air-alert_stats.html']

    def parse(self, response):
        # for alarm in response.xpath("/html/body/div[@class='wrapper']/table"):
        #     yield {
        #         "date_time": alarm.xpath("//td[1]/text()").extract(),
        #         "start_finish": alarm.xpath("//td[2]/text()").extract()
        #     }


        check_marker = response.xpath("/html/body/div[@class='wrapper']//td[2]/text()").extract()

        for _ in range(100): # number of scriped alarms
            yield {

                "date_time": response.xpath("/html/body/div[@class='wrapper']//td[1]/text()").extract(),
                "start_finish": response.xpath("/html/body/div[@class='wrapper']//td[2]/text()").extract()
            }


configure_logging()
runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(NewsSpider)
    yield runner.crawl(AirRaidAlarmsKyivSpider)
    reactor.stop()

crawl()
reactor.run() # the script will block here until the last crawl call is finished