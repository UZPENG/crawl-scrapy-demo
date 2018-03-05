# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy.utils.project import get_project_settings


class GuaziPipeline(object):
    def process_item(self, item, spider):
        settings = get_project_settings()
        # 配置必须大写字母不然报错
        host = settings['HOST']
        username = settings['USERNAME']
        password = settings['PASSWORD']
        database = settings['DATABASE']
        db = pymysql.connect(host, username, password, database, charset='utf8',
                             cursorclass=pymysql.cursors.DictCursor)
        cursor = db.cursor()
        sql = """INSERT INTO guazi(name, mileage, year, loc, origin_price, discount_price, img_url)
              VALUES ('%s', '%f', '%d', '%s', '%f', '%f', '%s')""" \
              % (item['name'], item['mileage'], item['year'], item['loc'],item['origin_price'], item['discount_price'], item['img_url'])
        cursor.execute(sql)

        db.commit()
        spider.logger.info("插入成功！")
        return item
