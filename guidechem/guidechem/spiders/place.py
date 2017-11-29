# -*- coding: utf-8 -*-
import codecs
import sys

import scrapy
from scrapy_redis.spiders import RedisSpider

from guidechem.items import BasicItem
from tool.tool import drop_bom

reload(sys)
sys.setdefaultencoding('utf8')
import re
_META_VERSION = 'v1.0'


class PlaceSpider(RedisSpider):
    name = "place"
    result_dir = './result'
    meta_version = _META_VERSION
    custom_settings = {
        'ITEM_PIPELINES': {
            'guidechem.pipelines.PlacePipeline': 300,
        },
        'AUTOTHROTTLE_ENABLED': True,
        'DOWNLOADER_MIDDLEWARES': {
            'guidechem.middlewares.AbuyunProxyMiddleware': 90,
        },
    }

    def start_requests(self):
        over = {}
        with codecs.open('done.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                over[line.strip()] = 1
        with codecs.open('notyet.txt', 'r', encoding='utf-8') as f:
            for kw in f.readlines():
                if kw.strip() in over:
                    continue

                # drop BOM header
                url_str = drop_bom(kw)

                yield scrapy.http.Request(
                    url='http://china.guidechem.com/product/list_keys-{}-p1.html'.format(url_str),
                    meta={'kw': kw.strip()},
                    callback=self.parse_detail
                )

    def parse_detail(self, response):
        item = BasicItem()
        item['kw'] = response.meta.get('kw')
        item['url'] = response.url
        places = response.css('div.main_serach_left div.seaec_titl_nav div.ec_tit_nvt ul li a::text').extract()
        place_dict = {}
        for place in places:
            place_name = re.search(r'(.*?)\((.*?)\)', place).group(1).strip()
            place_num = re.search(r'(.*?)\((.*?)\)', place).group(2).strip()
            place_dict[place_name] = place_num
        item['info'] = place_dict
        return item
