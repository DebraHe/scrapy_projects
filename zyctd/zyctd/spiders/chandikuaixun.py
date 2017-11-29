# -*- coding: utf-8 -*-
import scrapy
import os
import json
import codecs
from scrapy.shell import inspect_response
from zyctd.items import NewsItem
#from scrapy_redis.spiders import RedisSpider
# from tool import get_today
_META_VERSION = 'v1.0'


class ZyctdSpider(scrapy.Spider):
    name = "chandikuaixun"
    result_dir = './result'
    meta_version = _META_VERSION
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        "ITEM_PIPELINES": {
            'zyctd.pipelines.zyctd_chandikuaixun_Pipeline': 300,
        },
        'AUTOTHROTTLE_ENABLED': True,
    }

    def start_requests(self):
            # page = 1
        for page in range(695):
            yield scrapy.Request(
                url='http://www.zyctd.com/zixun/201-{}.html'.format(page)
            )

    def parse(self, response):
        for item_each in response.css('div#hasInfoRegion div.list li'):
            item = NewsItem()
            item['datePublished'] = item_each.css('span.g9::text').extract_first()
            item['headline'] = item_each.css('h2 a::text').extract_first()
            item['articleBody'] = item_each.css('p.info::text').extract_first().strip()
            item['url'] = item_each.css('h2 a::attr(href)').extract_first().encode('utf-8')
            yield item




