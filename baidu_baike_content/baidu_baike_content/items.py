# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BaiduBaikeContentItem(scrapy.Item):
    # define the fields for your item here like:
    raw_page_content = scrapy.Field()
    raw_url = scrapy.Field()
    raw_kw = scrapy.Field()
    raw_type = scrapy.Field()
    raw_main = scrapy.Field()

    raw_kw_type = scrapy.Field()


class BaiduBaikeDoubanItem(scrapy.Item):
    # define the fields for your item here like:
    raw_page_content = scrapy.Field()
    raw_url = scrapy.Field()
    raw_kw = scrapy.Field()
    raw_type = scrapy.Field()
    raw_main = scrapy.Field()

    raw_kw_type = scrapy.Field()
    raw_douban_id = scrapy.Field()
