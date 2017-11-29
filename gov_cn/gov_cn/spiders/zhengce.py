# -*- coding: utf-8 -*-

import urlparse

import scrapy

from gov_cn.items import GovCnItem
_META_VERSION = 'v1.0'


class GovCnSpider(scrapy.Spider):
    name = 'zhengce'
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
            url='http://sousuo.gov.cn/column/30469/0.htm',
            meta={'Bigtype': '政策_最新'}
        )

        yield scrapy.Request(
            url='http://sousuo.gov.cn/column/30474/0.htm',
            meta={'Bigtype': '政策_解读_部门'}
        )

        yield scrapy.Request(
            url='http://sousuo.gov.cn/column/30593/0.htm',
            meta={'Bigtype': '政策_解读_专家'}
        )

        yield scrapy.Request(
            url='http://sousuo.gov.cn/column/40048/0.htm',
            meta={'Bigtype': '政策_解读_媒体'}
        )

        yield scrapy.Request(
            url='http://sousuo.gov.cn/column/30142/0.htm',
            meta={'Bigtype': '政策_双创_国务院文件'}
        )

        yield scrapy.Request(
            url='http://sousuo.gov.cn/column/30209/0.htm',
            meta={'Bigtype': '政策_双创_权威解读'}
        )

        yield scrapy.Request(
            url='http://sousuo.gov.cn/column/30144/0.htm',
            meta={'Bigtype': '政策_双创_媒体解读'}
        )

        yield scrapy.Request(
            url='http://sousuo.gov.cn/column/30210/0.htm',
            meta={'Bigtype': '政策_双创_双创动态'}
        )

        yield scrapy.Request(
            url='http://sousuo.gov.cn/column/30080/0.htm',
            meta={'Bigtype': '政策_双创_办事指南'}
        )

    def parse(self, response):
        for each_item in response.css('ul.listTxt li'):
            title = each_item.css('h4 a::text').extract_first()
            time = each_item.css('h4 span.date::text').extract_first()
            yield scrapy.Request(
                url=each_item.css('h4 a::attr(href)').extract_first(),
                callback=self.parse_content,
                meta={'time': time, 'title': title, 'Bigtype': response.meta.get('Bigtype')}
            )
        next_page = response.css('a.next::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(
                url=next_page,
                meta={'Bigtype': response.meta.get('Bigtype')}
            )

    def parse_content(self, response):
        item = GovCnItem()
        item['datePublished'] = response.meta.get('time').strip()
        item['headline'] = response.meta.get('title')
        item['Bigtype'] = response.meta.get('Bigtype')
        item['articleBody'] = response.css('td.b12c').xpath('string(.)').extract_first()
        item['annex'] = [urlparse.urljoin(response.url, each_pic)for each_pic in response.css('td.b12c img::attr(src)').extract()]
        if not item['articleBody']:
            item['articleBody'] = response.css('div#UCAP-CONTENT').xpath('string(.)').extract_first()
            item['annex'] = [urlparse.urljoin(response.url, each_pic) for each_pic in
                             response.css('div#UCAP-CONTENT img::attr(src)').extract()]
        try:
            item['copyrightHolder'] = response.css('span.font::text').extract_first().split(u'：')[1].strip()
        except:
            item['copyrightHolder'] = ''
        item['url'] = response.url

        yield item