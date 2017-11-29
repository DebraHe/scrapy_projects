# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QinbingItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    priceValidUntil = scrapy.Field()
    fromLocation = scrapy.Field()
    price = scrapy.Field()
    datePublished = scrapy.Field()
    headline = scrapy.Field()
    articleBody = scrapy.Field()
    news_type = scrapy.Field()



