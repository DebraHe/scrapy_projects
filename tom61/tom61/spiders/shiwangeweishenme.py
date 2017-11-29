# -*- coding: utf-8 -*-
"""
反爬：无

爬取策略：通过target_utl.txt进入每一个需要爬取的页面，遍历所有词条进行爬取。

"""
import urlparse
import scrapy

from tom61.items import ShiwangeweishenmeItem

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

_META_VERSION = 'v1.0'


class ShiwangeweishenmeSpider(scrapy.Spider):
    name = "shiwangeweishenme"
    result_dir = './result'
    meta_version = _META_VERSION
    custom_settings = {
        'ITEM_PIPELINES': {
            'tom61.pipelines.ShiwangeweishenmePipeline': 300,
        },
        'AUTOTHROTTLE_ENABLED': True,
    }

    def start_requests(self):
        with open('doc/target_url.txt') as f:
            for line in f.readlines():
                yield scrapy.http.Request(
                    url=line.strip(),
                    callback=self.parse_list
                )

    def parse_list(self, response):
        list_urls = response.css('div#Mhead2_0 dl.txt_box dd a::attr(href)').extract()
        for list_url in list_urls:
            yield scrapy.http.Request(
                url=urlparse.urljoin(response.url, list_url),
                callback=self.parse_detail
            )
        next_page = response.css('div.t_fy a.nextpage::attr(href)').extract()
        if len(next_page) == 1:
            yield scrapy.http.Request(
                url=urlparse.urljoin(response.url, next_page[0]),
                callback=self.parse_list
            )
        elif len(next_page) == 2:
            yield scrapy.http.Request(
                url=urlparse.urljoin(response.url, next_page[1]),
                callback=self.parse_list
            )

    def parse_detail(self, response):
        if response.css('div.t_fy').extract():
            print response.url
        item = ShiwangeweishenmeItem()
        item['url'] = response.url
        item['title'] = response.css('div.t_news h1::text').extract_first()
        item['label'] = response.css('div.t_news div.t_news_top a::text').extract_first()
        item['data_time'] = response.css('div.t_news div.t_news_top b.topa::text').extract_first()
        item['description'] = response.css('div.t_news div.t_news_txt').xpath('string(.)').extract_first().strip()

        return item