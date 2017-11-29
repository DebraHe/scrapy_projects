# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GovCnItem(scrapy.Item):
    # define the fields for your item here like:
    copyrightHolder = scrapy.Field()
    datePublished = scrapy.Field()
    headline = scrapy.Field()
    articleBody = scrapy.Field()
    url = scrapy.Field()
    Bigtype = scrapy.Field()
    annex = scrapy.Field()
