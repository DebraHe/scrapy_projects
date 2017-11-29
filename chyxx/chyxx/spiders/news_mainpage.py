# -*- coding: utf-8 -*-

import urlparse

import scrapy

from chyxx.items import ChyxxItem
_META_VERSION = 'v1.0'


class ChyxxSpider(scrapy.Spider):
    name = 'news_mainpage'
    result_dir = './result'
    meta_version = _META_VERSION
    filename = name + '.json'
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'ITEM_PIPELINES': {
            'chyxx.pipelines.ChyxxPipeline': 300,
        },
        'AUTOTHROTTLE_ENABLED': False,
    }

    def start_requests(self):
        yield scrapy.Request(
            url='http://www.chyxx.com/industry/baozhuang1/',
            meta={'Bigtype': '包装主页头条'}
        )
        yield scrapy.Request(
            url='http://www.chyxx.com/industry/yinshua/',
            meta={'Bigtype': '印刷主页头条'}
        )
        yield scrapy.Request(
            url='http://www.chyxx.com/industry/zaozhi/',
            meta={'Bigtype': '造纸主页头条'}
        )
        yield scrapy.Request(
            url='http://www.chyxx.com/industry/mucai/',
            meta={'Bigtype': '木材主页头条'}
        )
        yield scrapy.Request(
            url='http://www.chyxx.com/industry/bzqt/',
            meta={'Bigtype': '包装其他主页头条'}
        )

    def parse(self, response):
        for each_item in response.css('div.headtitle h2 a'):
            title = each_item.css('a::text').extract_first()
            yield scrapy.Request(
                url='http://www.chyxx.com' + each_item.css('a::attr(href)').extract_first(),
                callback=self.parse_content,
                meta={'title': title, 'Bigtype': response.meta.get('Bigtype')}
            )

    def parse_content(self, response):
        item = ChyxxItem()
        item['datePublished'] = response.css('div.detail div.info span:nth-child(1)::text').extract_first().strip()
        item['headline'] = response.meta.get('title')
        item['Bigtype'] = response.meta.get('Bigtype')
        item['articleBody'] = response.css('div#contentBody').xpath('string(.)').extract_first().replace(u'中国产业信息网微信服务号', '').replace(u'中国产业信息网微信公众号', '').replace(response.css('div.content-info::text').extract_first(), '')
        item['annex'] = [urlparse.urljoin(response.url, each_pic)for each_pic in response.css('div#contentBody img::attr(src)').extract()]
        try:
            item['copyrightHolder'] = response.css('div.content-info::text').extract_first().split(u'：')[1]
        except:
            item['copyrightHolder'] = ''
        item['url'] = response.url
        yield item