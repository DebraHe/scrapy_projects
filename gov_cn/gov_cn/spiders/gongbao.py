# -*- coding: utf-8 -*-

import urlparse

import scrapy
import json

from gov_cn.items import GovCnItem
_META_VERSION = 'v1.0'


class GovCnSpider(scrapy.Spider):
    name = 'gongbao'
    result_dir = './result'
    filename = name + '.json'
    meta_version = _META_VERSION
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'ITEM_PIPELINES': {
            'gov_cn.pipelines.GovCnPipeline': 300,
        },
        'AUTOTHROTTLE_ENABLED': False,
    }

    def start_requests(self):
        yield scrapy.Request(
            url='http://www.gov.cn/gbgl/xhtml/js/gbgl.json',
            meta={'Bigtype': '政策_公报'}
        )

    def parse(self, response):
        for k, v in json.loads(response.text)[0].get('values').get('y2017').items():
            yield scrapy.Request(
                url='http://www.gov.cn' + v.get('gname'),
                callback=self.parse_list,
                meta={'Bigtype': response.meta.get('Bigtype')}
            )

    def parse_list(self, response):
        for each_item in response.css('ul.list01 li'):
            title = each_item.xpath('string(.)').extract_first()
            yield scrapy.Request(
                url='http://www.gov.cn' + each_item.css('a::attr(href)').extract_first(),
                callback=self.parse_content,
                meta={'title': title, 'Bigtype': response.meta.get('Bigtype')}
            )

    def parse_content(self, response):
        item = GovCnItem()
        item['datePublished'] = ''
        item['headline'] = response.meta.get('title')
        item['Bigtype'] = response.meta.get('Bigtype')
        item['articleBody'] = response.css('div#UCAP-CONTENT').xpath('string(.)').extract_first()
        item['annex'] = [urlparse.urljoin(response.url, each_pic)for each_pic in response.css('div#UCAP-CONTENT img::attr(src)').extract()]
        item['copyrightHolder'] = ''
        item['url'] = response.url

        yield item