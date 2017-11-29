# -*- coding: utf-8 -*-
"""
反爬：无

爬取策略：抓取API数据，爬取四小时后对数据进行筛选，选出不重复数据，下载并上传s3。

"""
import json
import urllib

import scrapy

from daily_english.items import DailyEnglishItem

_META_VERSION = 'v1.0'


class ContentSpider(scrapy.Spider):
    name = "content"
    result_dir = './result'
    meta_version = _META_VERSION
    custom_settings = {
        'ITEM_PIPELINES': {
            'daily_english.pipelines.DailyEnglishPipeline': 300,
        },
        'AUTOTHROTTLE_ENABLED': True,
    }

    def start_requests(self):
        params = {
            'showapi_appid': 'XXX',
            'showapi_sign': 'XXX',
            'count': '10',
        }
        url = 'http://route.showapi.com/1211-1?'
        api_url = url + urllib.urlencode(params)
        while True:
            yield scrapy.http.Request(
                url=api_url,
                dont_filter=True
            )

    def parse(self, response):
        datas = json.loads(response.text).get('showapi_res_body').get('data')
        for data in datas:
            item = DailyEnglishItem()
            item['url'] = response.url
            item['english'] = data.get('english')
            item['chinese'] = data.get('chinese')
            yield item

