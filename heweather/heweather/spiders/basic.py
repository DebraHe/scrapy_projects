# -*- coding: utf-8 -*-
"""
反爬：无

爬取策略：从城市txt中读取城市列表，调用和风天气API，获取相关数据，保存到MongoDB中。

"""
import json
import time
import scrapy

from tool.tool import get_the_file, clean_datas
from heweather.items import BasicItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
_META_VERSION = 'v1.0'


class BasicSpider(scrapy.Spider):
    name = "basic"
    result_dir = './result'
    filename = 'heweather_' + time.strftime('%Y%m%d', time.localtime(time.time())) + '.json'
    meta_version = _META_VERSION
    custom_settings = {
        'FILES_STORE': 's3://ruyi-scrapy/heweather/',
        'ITEM_PIPELINES': {
            # 'heweather.pipelines.HeweatherPipeline': 300,
            'heweather.pipelines.MongoDBPipeline': 300,
        },
        'AUTOTHROTTLE_ENABLED': True,
    }

    def start_requests(self):
        file_path = get_the_file(u"doc/china-city-list.json")
        with open(file_path) as f:
            city_infos = [json.loads(line.strip()) for line in f.readlines()]
        for city_info in city_infos:
            yield scrapy.http.Request(
                url='https://api.heweather.com/v5/weather?city={}&key=XXX'.format(city_info['id']),
                meta={'city_info': city_info}
            )

    # 调用 2560 次 和风API
    def parse(self, response):
        item = BasicItem()
        city_info = response.meta.get('city_info')
        weather_json = json.loads(response.text.encode('utf-8'))
        clean_data = clean_datas(weather_json)
        item['url'] = response.url
        item['city_info'] = city_info
        item['weather_info'] = clean_data
        return item