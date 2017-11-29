# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WordSolitaireItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    word = scrapy.Field()
    pinyin = scrapy.Field()
    expression = scrapy.Field()

