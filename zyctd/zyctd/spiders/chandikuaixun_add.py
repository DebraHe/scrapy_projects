# -*- coding: utf-8 -*-
import scrapy

from tool.tool import get_today
from zyctd.items import NewsItem
_META_VERSION = 'v1.0'


class ZyctdSpider(scrapy.Spider):
    name = "chandikuaixun_add"
    result_dir = './result'
    meta_version = _META_VERSION
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        "ITEM_PIPELINES": {
            'zyctd.pipelines.zyctd_chandikuaixun_MongoDBPipeline': 300,
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
            if item_each.css('span.g9::text').extract_first().split()[0] == get_today():
                item = NewsItem()
                item['datePublished'] = item_each.css('span.g9::text').extract_first()
                item['headline'] = item_each.css('h2 a::text').extract_first()
                item['articleBody'] = item_each.css('p.info::text').extract_first().strip()
                item['url'] = item_each.css('h2 a::attr(href)').extract_first().encode('utf-8')
                yield item




