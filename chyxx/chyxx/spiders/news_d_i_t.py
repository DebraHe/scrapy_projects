# -*- coding: utf-8 -*-
import urlparse

import scrapy

from chyxx.items import ChyxxItem
_META_VERSION = 'v1.0'


class ChyxxSpider(scrapy.Spider):
    name = 'news_d_i_t'
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
            url='http://www.chyxx.com/data/baozhuang1/',
            meta={'Bigtype': '包装行业数据'}
        )
        yield scrapy.Request(
            url='http://www.chyxx.com/data/yinshua/',
            meta={'Bigtype': '印刷行业数据'}
        )
        yield scrapy.Request(
            url='http://www.chyxx.com/data/zaozhi/',
            meta={'Bigtype': '造纸行业数据'}
        )
        yield scrapy.Request(
            url='http://www.chyxx.com/data/mucai/',
            meta={'Bigtype': '木材行业数据'}
        )
        yield scrapy.Request(
            url='http://www.chyxx.com/data/bzqt/',
            meta={'Bigtype': '包装其他行业数据'}
        )
        yield scrapy.Request(
            url='http://www.chyxx.com/industry/baozhuang1/1.html',
            meta={'Bigtype': '包装行业资讯'}
        )
        yield scrapy.Request(
            url='http://www.chyxx.com/industry/yinshua/1.html',
            meta={'Bigtype': '印刷行业资讯'}
        )
        yield scrapy.Request(
            url='http://www.chyxx.com/industry/zaozhi/1.html',
            meta={'Bigtype': '造纸行业资讯'}
        )
        yield scrapy.Request(
            url='http://www.chyxx.com/industry/mucai/1.html',
            meta={'Bigtype': '木材行业资讯'}
        )
        yield scrapy.Request(
            url='http://www.chyxx.com/industry/bzqt/1.html',
            meta={'Bigtype': '包装其他行业资讯'}
        )
        yield scrapy.Request(
            url='http://www.chyxx.com/top/baozhuang1/',
            meta={'Bigtype': '包装品牌排名'}
        )
        yield scrapy.Request(
            url='http://www.chyxx.com/top/yinshua/',
            meta={'Bigtype': '印刷品牌排名'}
        )
        yield scrapy.Request(
            url='http://www.chyxx.com/top/zaozhi/',
            meta={'Bigtype': '造纸品牌排名'}
        )
        yield scrapy.Request(
            url='http://www.chyxx.com/top/mucai/',
            meta={'Bigtype': '木材品牌排名'}
        )
        yield scrapy.Request(
            url='http://www.chyxx.com/top/bzqt/',
            meta={'Bigtype': '包装其他品牌排名'}
        )

    def parse(self, response):
        for each_item in response.css('div.pageList ul.list li'):
            title = each_item.css('a::text').extract_first()
            yield scrapy.Request(
                url='http://www.chyxx.com' + each_item.css('a::attr(href)').extract_first(),
                callback=self.parse_content,
                meta={'title': title, 'Bigtype': response.meta.get('Bigtype')}
            )
        next_page = response.xpath(u'//div[@class="pager pagerTop"]/a[text()="下一页"]/@href').extract_first()
        if next_page and next_page != 'javascript:void(0)':
            yield scrapy.Request(
                url='http://www.chyxx.com' + next_page,
                meta={'Bigtype': response.meta.get('Bigtype')}
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