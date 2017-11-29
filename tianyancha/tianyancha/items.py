# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TianyanchaItem(scrapy.Item):
    kw = scrapy.Field()
    name = scrapy.Field()
    item_url = scrapy.Field()
    source_url = scrapy.Field()
    legal = scrapy.Field()
    capital = scrapy.Field()
    registration_date = scrapy.Field()
    # addr = scrapy.Field()
    status = scrapy.Field()
    province = scrapy.Field()


class TianyanchaDetailItem(scrapy.Item):
    source_url = scrapy.Field()
    name = scrapy.Field()
    addr = scrapy.Field()
    phone = scrapy.Field()
    email = scrapy.Field()
    website = scrapy.Field()
    raw_background = scrapy.Field()
    reg_id = scrapy.Field()
    org_id = scrapy.Field()
    credit_id = scrapy.Field()
    company_type = scrapy.Field()
    taxpayer_id = scrapy.Field()
    industry = scrapy.Field()
    expiry = scrapy.Field()
    check_date = scrapy.Field()
    reg_org = scrapy.Field()
    reg_addr = scrapy.Field()
    scope = scrapy.Field()
    score = scrapy.Field()
    staff = scrapy.Field()

    staff_people = scrapy.Field()
    invest = scrapy.Field()

    gudong = scrapy.Field()
    biangeng = scrapy.Field()
    rongzi = scrapy.Field()
    team_member = scrapy.Field()
    firmProduct = scrapy.Field()
    touzi_event = scrapy.Field()
    lawsuit = scrapy.Field()
    jingpin = scrapy.Field()
    court = scrapy.Field()
    zhixing = scrapy.Field()
    announcementcourt = scrapy.Field()
    equity = scrapy.Field()
    bid = scrapy.Field()
    recruit = scrapy.Field()
    taxcredit = scrapy.Field()
    check = scrapy.Field()
    product_info = scrapy.Field()
    certificate = scrapy.Field()
    wechat = scrapy.Field()
    tmInfo = scrapy.Field()
    patent = scrapy.Field()
    copyright = scrapy.Field()
    copyrightWorks = scrapy.Field()
    icp = scrapy.Field()
