# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EncvsItem(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    release_time = scrapy.Field()
    source = scrapy.Field()
    content = scrapy.Field()
    enclosure = scrapy.Field()
