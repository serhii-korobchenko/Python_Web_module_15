import scrapy
from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging

class AirRaidAlarmsKyivSpider(scrapy.Spider):
    name = 'air_raid_alarms_kyiv'

    # start custom settings
    custom_settings = {


        # 'ITEM_PIPELINES': {
        # 'serhii_spyder_bot.pipelines.SerhiiSpyderBotPipeline': 300
        #                    },

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


        yield {

            "date_time": response.xpath("/html/body/div[@class='wrapper']//td[1]/text()").extract(),
            "start_finish": response.xpath("/html/body/div[@class='wrapper']//td[2]/text()").extract()
        }


configure_logging()
runner = CrawlerRunner()

@defer.inlineCallbacks
def crawl():
    yield runner.crawl(AirRaidAlarmsKyivSpider)
    #yield runner.crawl(AuthorsDetailSpider)
    reactor.stop()

crawl()
reactor.run() # the script will block here until the last crawl call is finished