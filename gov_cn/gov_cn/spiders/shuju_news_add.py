# -*- coding: utf-8 -*-

import urlparse


import datetime
import scrapy

from gov_cn.items import GovCnItem
_META_VERSION = 'v1.0'


class GovCnSpider(scrapy.Spider):
    name = 'shuju_news_add'
    result_dir = './result'
    filename = name + '.json'
    meta_version = _META_VERSION
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'ITEM_PIPELINES': {
            'gov_cn.pipelines.MongoDBPipeline': 300,
        },
        'AUTOTHROTTLE_ENABLED': False,
    }

    def start_requests(self):
        yield scrapy.Request(
            url='http://sousuo.gov.cn/column/40535/0.htm',
            meta={'Bigtype': '数据_数据快递'}
        )

        yield scrapy.Request(
            url='http://sousuo.gov.cn/column/30722/0.htm',
            meta={'Bigtype': '数据_数据要闻'}
        )

    def parse(self, response):
        for each_item in response.css('ul.listTxt li'):
            title = each_item.css('h4 a::text').extract_first()
            time = each_item.css('h4 span.date::text').extract_first()
            if time == datetime.date.today().strftime("%Y.%m.%d"):
                yield scrapy.Request(
                    url=each_item.css('h4 a::attr(href)').extract_first(),
                    callback=self.parse_content,
                    meta={'time': time, 'title': title, 'Bigtype': response.meta.get('Bigtype')}
                )

    def parse_content(self, response):
        item = GovCnItem()
        item['datePublished'] = response.css('div.pages-date::text').extract_first().strip()
        item['headline'] = response.meta.get('title')
        item['Bigtype'] = response.meta.get('Bigtype')
        item['articleBody'] = response.css('div#UCAP-CONTENT').xpath('string(.)').extract_first()
        item['annex'] = [urlparse.urljoin(response.url, each_pic) for each_pic in
                         response.css('div#UCAP-CONTENT img::attr(src)').extract()]
        try:
            item['copyrightHolder'] = response.css('span.font::text').extract_first().split(u'：')[1].strip()
        except:
            item['copyrightHolder'] = ''
        item['url'] = response.url
        yield item