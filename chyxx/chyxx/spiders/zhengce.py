# -*- coding: utf-8 -*-

import urlparse

import scrapy

from chyxx.items import ChyxxItem
_META_VERSION = 'v1.0'


class ChyxxSpider(scrapy.Spider):
    name = 'zhengce'
    result_dir = './result'
    filename = name + '.json'
    meta_version = _META_VERSION
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'ITEM_PIPELINES': {
            'chyxx.pipelines.ChyxxPipeline': 300,
        },
        'AUTOTHROTTLE_ENABLED': False,
    }

    def start_requests(self):
        for page in range(1, 42):
            yield scrapy.Request(
                url='http://www.chyxx.com/zhengce/{}.html'.format(page),
                meta={'Bigtype': '包装行业政策'}
            )

    def parse(self, response):
        for each_item in response.css('div.pageList ul.list li'):
            title = each_item.css('a:nth-child(2)::text').extract_first()
            yield scrapy.Request(
                url=each_item.css('a:nth-child(2)::attr(href)').extract_first(),
                callback=self.parse_content,
                meta={'title': title, 'Bigtype': response.meta.get('Bigtype')}
            )

    def parse_content(self, response):
        item = ChyxxItem()
        item['datePublished'] = response.css('div.detail div.info span:nth-child(1)::text').extract_first().strip()
        item['headline'] = response.meta.get('title')
        item['Bigtype'] = response.meta.get('Bigtype')
        item['articleBody'] = response.css('div#contentBody').xpath('string(.)').extract_first().replace(u'中国产业信息网微信服务号', '').replace(u'中国产业信息网微信公众号', '').replace(response.css('div.content-info::text').extract_first(), '')
        try:
            item['copyrightHolder'] = response.css('div.content-info::text').extract_first().split(u'：')[1]
        except:
            item['copyrightHolder'] = ''
        item['annex'] = [urlparse.urljoin(response.url, each_pic)for each_pic in response.css('div#contentBody img::attr(src)').extract()]
        item['url'] = response.url
        yield item