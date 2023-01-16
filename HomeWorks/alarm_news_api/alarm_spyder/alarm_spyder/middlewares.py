# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from copy import copy, deepcopy
from datetime import datetime
import re

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class AlarmSpyderSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        try:
            new_list = []
            flag = 0
            flag_global_iteration = 0

            for i in result:

                # print(f'-----------------RESULT______{i}')
                # print(f'-----------------TYPE______{type(i)}')

                if type(i) is dict:

                    #print(len(i.values()))
                    #print(type(i.values()))
                    my_list = list(i.values())
                    #print (type(my_list))
                    temp_list = []
                    for number in range (0, len(my_list[0])):


                        if my_list[1][number-1] != my_list[1][number]:
                            if my_list[1][number] == '🟢 Відбій тривоги' :
                                #print (my_list[0][number], '0')
                                temp_list.append(my_list[0][number])
                                temp_list.append(0)
                                new_list.append(temp_list)
                                temp_list = []
                            else:
                                #print(my_list[0][number], '1')
                                temp_list.append(my_list[0][number])
                                temp_list.append(1)
                                new_list.append(temp_list)
                                temp_list = []

                    #new_list_reversed = list(reversed(new_list)) #reversing alarm order
                    new_list_reversed = new_list
                    updated_list_outter = []
                    updated_list_inner = []

                    for item in range(1,len(new_list_reversed), 2):
                        flag += 1
                        name_alarm = 'Alarm' + str(len(my_list[0])-flag)

                        updated_list_inner.append(name_alarm)

                        updated_list_inner.append(new_list_reversed[item][0])
                        updated_list_inner.append(new_list_reversed[item - 1][0])
                        updated_list_outter.append(updated_list_inner)
                        updated_list_inner = []


                    i['result'] = updated_list_outter

                for key, value in i.items():
                    if key == 'result':
                        for item_in_list in value:
                            # print(len(value))
                            if item_in_list == value[flag_global_iteration]:
                                my_list = deepcopy(value[flag_global_iteration])

                        value.clear()
                        for r in my_list:
                            if re.search("\d\d:\d\d \d\d.\d\d.\d\d", r):
                                date_temp_list = r.split(' ')
                                reversed_date = str(date_temp_list[1])+" "+str(date_temp_list[0])
                                value.append(reversed_date)
                            else:
                                value.append(r)
                        #print(f'Length of {key}: {len(value)}')
                    else:
                        value.clear()

                flag = 0
                flag_global_iteration += 1
                yield i



        except Exception as err:
            print(f"Unexpected alarm {err=}, {type(err)=}")


    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class AlarmSpyderDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)



class NewsSpyderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        try:
            new_list = []
            flag = 0

            for i in result:
                # print(f'-----------------RESULT______{i}')
                # print(f'-----------------TYPE______{type(i)}')
                for key, value in i.items():
                    if key == 'date_time':
                        for item_list in value:
                            if item_list.strip() == 'оновлено':
                                value.remove(item_list)

                    #print(f'Length of {key}: {len(value)}')

                for key, value in i.items():
                    for item_list in value:
                        #print(len(value))
                        if item_list == value[flag]:
                            my_item = copy(value[flag].strip())

                    value.clear()
                    value.append(my_item)
                    print(f'Length of {key}: {len(value)}')

                flag += 1
                yield i

        except Exception as err:
            print(f"Unexpected news{err=}, {type(err)=}")
    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)