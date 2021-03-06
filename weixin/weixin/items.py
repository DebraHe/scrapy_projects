# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    headline = scrapy.Field()
    articleBody = scrapy.Field()
    datePublished = scrapy.Field()
    url = scrapy.Field()
    copyrightHolder = scrapy.Field()
    author = scrapy.Field()
    publisher = scrapy.Field()
    annex = scrapy.Field()
    kind = scrapy.Field()
