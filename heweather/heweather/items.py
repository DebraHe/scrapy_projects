# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BasicItem(scrapy.Item):
    # define the fields for your item here like:
    weather_info = scrapy.Field()
    city_info = scrapy.Field()
    url = scrapy.Field()



