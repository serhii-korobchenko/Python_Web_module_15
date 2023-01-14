import scrapy
#from quotes_js_scraper.items import QuoteItem
from scrapy_selenium import SeleniumRequest


class NewsSpider(scrapy.Spider):
    name = 'news__'

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
        }

        # "SPIDER_MIDDLEWARES": {
        #     'alarm_spyder.middlewares.AlarmSpyderSpiderMiddleware': 543,
        # }
    }
    # stop custom settings

    def start_requests(self):
        url = 'https://www.unian.ua/tag/kijiv'
        yield SeleniumRequest(url=url, callback=self.parse, wait_time=10)
#script='window.scrollTo(0, document.body.scrollHeight);
    # allowed_domains = ['unian.ua']
    # start_urls = ['https://www.unian.ua/tag/kijiv']

    def parse(self, response):
        for outer in range(1,2):
            for item in range(1,21):
            #for quote in response.xpath("//*[@id='block_left_column_content']/div[1]"):
                # yield {
                #     "author": quote.xpath("span/small/text()").extract()
                # }
                about_link = response.xpath(f"//*[@id='block_left_column_content']/div/div[{item}]/div/h3/a/@href").get()
                # if about_link:
                #     yield scrapy.Request(url=about_link, callback=self.parse_detail)


                yield {
                    "news_title": response.xpath(f'//*[@id="block_left_column_content"]/div[{outer}]/div[{item}]/div/h3/a[@class="list-thumbs__title"]/text()').extract(),
                    "date_time": response.xpath(f'//*[@id="block_left_column_content"]/div[{outer}]/div[{item}]/div/div/text()').extract()

                               }

        # next_link = response.xpath("//li[@class='next']/a/@href").get()
        # if next_link:
        #     yield scrapy.Request(url=self.start_urls[0] + next_link)

    def parse_detail(self, response):

        yield {
            "news_title": response.xpath('//*[@id="block_left_column_content"]//h1/text()').extract(),
            "date_time": response.xpath('//*[@id="block_left_column_content"]/div/div/div[2]/div[1]/div/text()').extract()

        }