# -*- coding: utf-8 -*-

import urlparse


import datetime
import scrapy

from gov_cn.items import GovCnItem
_META_VERSION = 'v1.0'


class GovCnSpider(scrapy.Spider):
    name = 'xinwen_add'
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
            url='http://sousuo.gov.cn/column/31421/0.htm',
            meta={'Bigtype': '新闻_要闻'}
        )

        yield scrapy.Request(
            url='http://sousuo.gov.cn/column/30902/0.htm',
            meta={'Bigtype': '新闻_政务联播_地方'}
        )

        yield scrapy.Request(
            url='http://sousuo.gov.cn/column/30613/0.htm',
            meta={'Bigtype': '新闻_政务联播_部门'}
        )

        yield scrapy.Request(
            url='http://sousuo.gov.cn/column/30618/0.htm',
            meta={'Bigtype': '新闻_新闻发布_部门'}
        )

        yield scrapy.Request(
            url='http://sousuo.gov.cn/column/30619/0.htm',
            meta={'Bigtype': '新闻_新闻发布_其他'}
        )

        yield scrapy.Request(
            url='http://sousuo.gov.cn/column/30614/0.htm',
            meta={'Bigtype': '新闻_人事信息_中央'}
        )

        yield scrapy.Request(
            url='http://sousuo.gov.cn/column/30627/0.htm',
            meta={'Bigtype': '新闻_人事信息_地方'}
        )

        yield scrapy.Request(
            url='http://sousuo.gov.cn/column/30615/0.htm',
            meta={'Bigtype': '新闻_人事信息_驻外'}
        )

        yield scrapy.Request(
            url='http://sousuo.gov.cn/column/30616/0.htm',
            meta={'Bigtype': '新闻_人事信息_其他'}
        )

        yield scrapy.Request(
            url='http://sousuo.gov.cn/column/30611/0.htm',
            meta={'Bigtype': '新闻_滚动'}
        )

        yield scrapy.Request(
            url='http://sousuo.gov.cn/column/30661/0.htm',
            meta={'Bigtype': '新闻_图解_国务院常务会'}
        )

        yield scrapy.Request(
            url='http://sousuo.gov.cn/column/30662/0.htm',
            meta={'Bigtype': '新闻_图解_总理活动'}
        )

        yield scrapy.Request(
            url='http://sousuo.gov.cn/column/30663/0.htm',
            meta={'Bigtype': '新闻_图解_政策'}
        )

        yield scrapy.Request(
            url='http://sousuo.gov.cn/column/30665/0.htm',
            meta={'Bigtype': '新闻_图解_其他'}
        )

    def parse(self, response):
        for each_item in response.css('ul.listTxt li'):
            title = each_item.css('h4 a::text').extract_first()
            time = each_item.css('h4 span.date::text').extract_first()
            if time == datetime.date.today().strftime("%Y.%m.%d"):
                yield scrapy.Request(
                    url=each_item.css('h4 a::attr(href)').extract_first(),
                    callback=self.parse_content,
                    meta={'title': title, 'Bigtype': response.meta.get('Bigtype') }
                )

    def parse_content(self, response):
        item = GovCnItem()
        item['datePublished'] = response.css('div.pages-date::text').extract_first().strip()
        item['headline'] = response.meta.get('title')
        item['Bigtype'] = response.meta.get('Bigtype')
        item['articleBody'] = response.css('div#UCAP-CONTENT').xpath('string(.)').extract_first()
        item['annex'] = [urlparse.urljoin(response.url, each_pic)for each_pic in response.css('div#UCAP-CONTENT img::attr(src)').extract()]
        try:
            item['copyrightHolder'] = response.css('span.font::text').extract_first().split(u'：')[1].strip()
        except:
            item['copyrightHolder'] = ''
        item['url'] = response.url
        yield item