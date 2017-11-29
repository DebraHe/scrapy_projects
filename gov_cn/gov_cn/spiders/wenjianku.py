# -*- coding: utf-8 -*-

import urlparse

import scrapy

from gov_cn.items import GovCnItem
_META_VERSION = 'v1.0'


class GovCnSpider(scrapy.Spider):
    name = 'wenjianku'
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
            url='http://sousuo.gov.cn/list.htm?q=&n=100&p={}&t=paper&sort=pubtime&childtype=&subchildtype=&pcodeJiguan=&pcodeYear=&pcodeNum=&location=&searchfield=&title=&content=&pcode=&puborg=&timetype=timeqb&mintime=&maxtime='.format(0),
            meta={'Bigtype': '政策_文件库'}
        )

    def parse(self, response):
        for each_item in response.css('div.dataBox tr'):
            title = each_item.css('td.info a::text').extract_first()
            if title:
                time = each_item.css('td:nth-child(5)::text').extract_first()
                yield scrapy.Request(
                    url=each_item.css('td.info a::attr(href)').extract_first(),
                    callback=self.parse_content,
                    meta={'time': time, 'title': title, 'Bigtype': response.meta.get('Bigtype')}
                )
        next_page = response.css('span.nav_go_next a::attr(href)').extract_first()
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
        item['annex'] = [urlparse.urljoin(response.url, each_pic) for each_pic in
                         response.css('td.b12c img::attr(src)').extract()]
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