# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class IdaddyDetailItem(scrapy.Item):
    # define the fields for your item here like:
    idaddy_id = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    album_id = scrapy.Field()
    chapter_id = scrapy.Field()
    track_in_albun = scrapy.Field()
    track_title = scrapy.Field()
    play_time = scrapy.Field()
    episodes = scrapy.Field()
    intro = scrapy.Field()
    rating_number = scrapy.Field()
    Type = scrapy.Field()
    first_level = scrapy.Field()
    second_level = scrapy.Field()
    row_number = scrapy.Field()
    cats = scrapy.Field()
