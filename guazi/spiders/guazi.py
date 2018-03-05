from scrapy import Spider
from scrapy import Request
import re
from guazi.items import GuaziItem
from datetime import datetime
import time
from selenium import webdriver


class guazi(Spider):
    name = 'guazi'
    base_url = 'https://www.guazi.com'
    driver = None
    page = 1

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)

        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--proxy-server=socks5://172.29.108.123:1080')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)

    def start_requests(self):
        urls = ['https://www.guazi.com/www/buy/o1i7/#bread']
        for url in urls:
            self.logger.info('开始请求。。。')
            request = Request(url=url, callback=self.parse)
            yield request

    def parse(self, response):
        with open('response.html', 'rw') as result:
            result.write(response)
        hour = datetime.now().hour
        self.logger.info('返回结果成功开始解释。。。')
        while hour in range(8):
            self.logger.info('时间段不合适，开始睡眠。。。')
            time.sleep(3600)
            hour = datetime.now().hour

        car_list = response.css('.carlist').xpath('.//li')
        pattern = '[0-9\.]+'

        self.logger.info('汽车列表大小' + str(len(car_list)) + ',遍历汽车列表。。。')
        for car in car_list:
            name = car.css('.t::text').extract()[0]
            img_src = car.xpath('.//img/@src').extract()[0]
            info = car.css('.t-i::text').extract()
            year = re.match(pattern=pattern, string=info[0]).group()
            mileage = re.match(pattern=pattern, string=info[1]).group()
            loc = info[2]
            discount_price = car.css('.t-price').xpath('./p/text()').extract()[0]
            tmp = car.css('.line-through::text').extract()
            if len(tmp) != 0:
                origin_price = re.match(pattern=pattern, string=tmp[0]).group()
            else:
                origin_price = '0.0'
            car_item = GuaziItem()
            car_item['name'] = name
            car_item['img_url'] = img_src
            car_item['year'] = int(year)
            car_item['mileage'] = float(mileage)
            car_item['loc'] = loc
            car_item['discount_price'] = float(discount_price)
            car_item['origin_price'] = float(origin_price)

            yield self.make_car_item(car_item=car_item)

        page_link = response.css('.pageLink').xpath(".//li[@class='link-on']/following-sibling::*")
        next_link = page_link.xpath(".//a/@href").extract()[0]
        self.logger.info('找到下一页，url为' + next_link + ' 开始请求下一页。。。')

        if next_link is not None:
            page_no = re.search('o[0-9]+', next_link).group()[1:]
            if int(page_no) < self.page:
                with open('error.html', 'rw') as file:
                    file.write(response)
                self.logger.info('页面序号错误，程序终止。。。')
                exit(0)

            request = Request(url=self.base_url + next_link, callback=self.parse)
            self.page += 1
            yield request

    def make_car_item(self, car_item):
        return car_item

    @staticmethod
    def close(spider, reason):
        spider.driver.quit()
        return super().close(spider, reason)
