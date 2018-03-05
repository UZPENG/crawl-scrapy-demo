# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse
import time


class GuaziDownloaderMiddleware(object):

    def process_request(self, request, spider):
        driver = spider.driver
        driver.get(request.url)

        time.sleep(5)

        return HtmlResponse(url=driver.current_url, body=driver.page_source, encoding='utf-8')


class GuaziProxy(object):
    def process_request(self, request, spider):
        request.meta['proxy'] = 'http://172.29.108.123:1080'
        return request
