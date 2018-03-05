# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GuaziItem(scrapy.Item):
    img_url = scrapy.Field()
    name = scrapy.Field()
    year = scrapy.Field()
    mileage = scrapy.Field()
    loc = scrapy.Field()
    discount_price = scrapy.Field()
    origin_price = scrapy.Field()
