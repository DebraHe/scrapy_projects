# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QingtingDetailItem(scrapy.Item):
    title = scrapy.Field()
    qingting_channel_id = scrapy.Field()
    qingting_programs_id = scrapy.Field()
    tracks = scrapy.Field()
    track_title = scrapy.Field()
    play_time = scrapy.Field()
    play_count = scrapy.Field()
    update_time = scrapy.Field()
    last_update = scrapy.Field()
    anchor_cover_pic = scrapy.Field()
    anchor_name = scrapy.Field()
    mediainfo = scrapy.Field()
    url = scrapy.Field()
