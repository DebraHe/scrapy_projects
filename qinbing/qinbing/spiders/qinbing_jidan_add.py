# -*- coding: utf-8 -*-
import urlparse

import re

import datetime
import scrapy
import time
from qinbing.items import QinbingItem

_META_VERSION = 'v1.0'


class QinBingSpider(scrapy.Spider):
    name = 'qinbing_jidan_add'
    result_dir = './result'
    meta_version = _META_VERSION
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'ITEM_PIPELINES': {
            'qinbing.pipelines.Qinbing_jidan_MongoDBPipeline': 300,
        },
        'AUTOTHROTTLE_ENABLED': False,
    }

    def start_requests(self):
        for page in range(1, 16):
            yield scrapy.Request(
                url='http://www.qinbing.cn/jidanjiage/{}'.format(page)
            )

    def parse(self, response):
        for each_item in response.css('div.zx_left1 div.list0 div.list2 a.cb6'):
            title = each_item.css('a::attr(title)').extract_first()
            is_match = re.match(ur'\d+月\d+日(黑龙江|吉林|辽宁)', title)
            if is_match:
                time = each_item.xpath('../../div[@class="list3"]//text()').extract_first().strip()
                if time.split()[0] == datetime.date.today().strftime("%Y/%m/%d"):
                    yield scrapy.Request(
                        url=urlparse.urljoin(response.url, each_item.css('a::attr(href)').extract_first()),
                        callback=self.parse_content,
                        meta={'time': time}
                    )

    def parse_content(self, response):
        priceValidUntil = time.strftime("%Y年%m月%d日", time.strptime(response.meta.get('time'), "%Y/%m/%d %H:%M:%S"))
        for each_item in response.css('div#pastingspan1 table tr'):
            fromLocation = each_item.css('td:nth-child(1)').xpath('string(.)').extract_first()
            price = each_item.css('td:nth-child(2)::text').extract_first()
            if price and fromLocation != u'报价地区':
                item = QinbingItem()
                item['priceValidUntil'] = priceValidUntil
                item['fromLocation'] = fromLocation
                item['price'] = price
                item['url'] = response.url
                yield item