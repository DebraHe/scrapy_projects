# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LyricItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    id = scrapy.Field()
    raw_lyric = scrapy.Field()


class CommentItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    id = scrapy.Field()
    user_name = scrapy.Field()
    content = scrapy.Field()
    com_time = scrapy.Field()
    praise_num = scrapy.Field()