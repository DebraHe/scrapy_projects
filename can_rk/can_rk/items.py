# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CanRkItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    id = scrapy.Field()
    caseCode = scrapy.Field()
    caseState = scrapy.Field()
    execCourtName = scrapy.Field()
    execMoney = scrapy.Field()
    partyCardNum = scrapy.Field()
    pname = scrapy.Field()
    caseCreateTime = scrapy.Field()


class CanRk_shixin_Item(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    id = scrapy.Field()
    iname = scrapy.Field()
    caseCode = scrapy.Field()
    age = scrapy.Field()
    sexy = scrapy.Field()
    cardNum = scrapy.Field()
    courtName = scrapy.Field()
    areaName = scrapy.Field()
    partyTypeName = scrapy.Field()
    gistId = scrapy.Field()
    regDate = scrapy.Field()
    gistUnit = scrapy.Field()
    duty = scrapy.Field()
    performance = scrapy.Field()
    performedPart = scrapy.Field()
    unperformPart = scrapy.Field()
    disruptTypeName = scrapy.Field()
    publishDate = scrapy.Field()


class CanRk_wenshu_Item(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    kw = scrapy.Field()
    time = scrapy.Field()
    raw_data = scrapy.Field()
    content = scrapy.Field()
