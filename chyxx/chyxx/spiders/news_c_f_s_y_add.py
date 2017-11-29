# -*- coding: utf-8 -*-

import urlparse
import datetime
import scrapy
from chyxx.items import ChyxxItem
_META_VERSION = 'v1.0'


class ChyxxSpider(scrapy.Spider):
    name = 'news_c_f_s_y_add'
    filename = name + '.json'
    result_dir = './result'
    meta_version = _META_VERSION
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'ITEM_PIPELINES': {
            'chyxx.pipelines.MongoDBPipeline': 300,
        },
        'AUTOTHROTTLE_ENABLED': False,
    }

    def start_requests(self):
        yield scrapy.Request(
            url='http://www.chyxx.com/news/chuangxin/baozhuang/list_1.html',
            meta={'Bigtype': '包装行业创新'}
        )

        yield scrapy.Request(
            url='http://www.chyxx.com/news/fenxi/baozhuang/list_1.html',
            meta={'Bigtype': '包装行业分析'}
        )

        yield scrapy.Request(
            url='http://www.chyxx.com/news/shichang/baozhuang/list_1.html',
            meta={'Bigtype': '包装市场环境'}
        )

        yield scrapy.Request(
            url='http://www.chyxx.com/news/yujing/baozhuang/list_1.html',
            meta={'Bigtype': '包装产业预警'}
        )

    def parse(self, response):
        for each_item in response.css('div.pageList ul.list-pic-title li.clearfix'):
            title = each_item.css('h3 a::text').extract_first()
            time = each_item.css('span.date::text').extract_first()
            if time.split()[0] == datetime.date.today().strftime("%Y-%m-%d"):
                yield scrapy.Request(
                    url=urlparse.urljoin(response.url, each_item.css('h3 a::attr(href)').extract_first()),
                    callback=self.parse_content,
                    meta={'time': time, 'title': title, 'Bigtype': response.meta.get('Bigtype')}
                )

    def parse_content(self, response):
        item = ChyxxItem()
        item['datePublished'] = response.meta.get('time').strip()
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