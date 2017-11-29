# -*- coding: utf-8 -*-
import scrapy
import os
import json
import codecs
from scrapy.shell import inspect_response
from yt1998.items import NewsItem
#from scrapy_redis.spiders import RedisSpider
# from tool import get_today
_META_VERSION = 'v1.0'


class YaotongSpider(scrapy.Spider):
    name = "tiantianhangqing"
    result_dir = './result'
    meta_version = _META_VERSION
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        "ITEM_PIPELINES": {
            'yt1998.pipelines.Yt1998_tiantianhangqing_Pipeline': 300,
        },
        'AUTOTHROTTLE_ENABLED': True,
    }

    def start_requests(self):
        for page in range(310):
            yield scrapy.Request(
                url='http://www.yt1998.com/ytw/second/marketMgr/query.jsp?random=0.697085111618426&scid=1&lmid=3&ycnam=&times=1&pageIndex={}&pageSize=10'.format(page)
            )
            yield scrapy.Request(
                url='http://www.yt1998.com/ytw/second/marketMgr/query.jsp?random=0.20438839782710327&scid=2&lmid=3&ycnam=&times=2&pageIndex={}&pageSize=10'.format(
                    page)
            )
            yield scrapy.Request(
                url='http://www.yt1998.com/ytw/second/marketMgr/query.jsp?random=0.2918444071145532&scid=4&lmid=3&ycnam=&times=3&pageIndex={}&pageSize=10'.format(
                    page)
            )
            yield scrapy.Request(
                url='http://www.yt1998.com/ytw/second/marketMgr/query.jsp?random=0.13848115066174982&scid=3&lmid=3&ycnam=&times=4&pageIndex={}&pageSize=10'.format(
                    page)
            )

    def parse(self, response):
        content = json.loads(response.text).get('data')
        for item_each in content:
            item = NewsItem()
            item['datePublished'] = item_each.get('dtm')
            item['raw_data'] = item_each
            item['headline'] = item_each.get('title')
            item['articleBody'] = item_each.get('cont').replace(u'&nbsp;', '')
            item['copyrightHolder'] = item_each.get('source')
            item['url'] = 'http://www.yt1998.com/minute--' + item_each.get('acid') + '--1.html'
            yield item

