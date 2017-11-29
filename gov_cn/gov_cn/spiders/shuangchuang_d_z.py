# -*- coding: utf-8 -*-

import urlparse

import scrapy

from gov_cn.items import GovCnItem
_META_VERSION = 'v1.0'


class GovCnSpider(scrapy.Spider):
    name = 'shuangchuang_d_z'
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
            url='http://www.gov.cn/zhengce/zhuti/shuangchuang/dfwj.htm',
            meta={'Bigtype': '政策_双创_地方文件'}
        )
        yield scrapy.Request(
            url='http://www.gov.cn/zhengce/zhuti/shuangchuang/buwei.htm',
            meta={'Bigtype': '政策_双创_部委文件'}
        )

    def parse(self, response):
        for each_item in response.css('div.container1 a'):
            yield scrapy.Request(
                url='http://www.gov.cn' + each_item.css('a::attr(href)').extract_first(),
                callback=self.parse_more,
                meta={'Bigtype': response.meta.get('Bigtype')}
            )

    def parse_more(self, response):
        yield scrapy.Request(
            url=response.css('span.shortId a::attr(href)').extract_first(),
            callback=self.parse_list,
            meta={'Bigtype': response.meta.get('Bigtype')}
        )

    def parse_list(self, response):
        for each_item in response.css('ul.listTxt li'):
            title = each_item.css('h4 a::text').extract_first()
            yield scrapy.Request(
                url=each_item.css('h4 a::attr(href)').extract_first(),
                callback=self.parse_content,
                meta={'title': title, 'Bigtype': response.meta.get('Bigtype') }
            )
        next_page = response.css('a.next::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(
                url=next_page,
                meta={'Bigtype': response.meta.get('Bigtype')}
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