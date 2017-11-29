# -*- coding: utf-8 -*-
import codecs
import scrapy
import urllib2
import urlparse
from baidu_baike_content.items import BaiduBaikeContentItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
_META_VERSION = 'v1.0'


class ContentSpider(scrapy.Spider):
    name = "content"
    result_dir = './result'
    meta_version = _META_VERSION
    custom_settings = {
        'ITEM_PIPELINES': {
            'baidu_baike_content.pipelines.BaiduBaikeContentPipeline': 300,
        },
        'AUTOTHROTTLE_ENABLED': True,
    }

    def start_requests(self):
        reqs = []
        over = {}
        with codecs.open('doc/done.txt', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                over[line.strip()] = 1
        with codecs.open('doc/notyet.txt', 'r', encoding='utf-8') as f:
            for kw in f.readlines():
                if kw.strip() in over:
                    continue

                # drop BOM header
                urlstr = urllib2.quote(kw.strip().encode('utf-8'))
                if urlstr[:9] == '%EF%BB%BF':
                    urlstr = urlstr[9:]

                reqs.append(scrapy.http.Request(
                    url='https://baike.baidu.com/item/{}'.format(urlstr),
                    meta={'kw': kw.strip()}
                ))
        self.logger.info('total {}'.format(len(reqs)))
        return reqs

    def parse(self, response):
        # not jump to the no word page
        is_content = response.css('div.create-entrance')
        if not is_content:
            has_type = response.css('ul.polysemantList-wrapper')
            # for those name has no type right after the name
            self.logger.info('crawl {}'.format(response.url))
            yield scrapy.http.Request(
                url=response.url,
                meta={'kw': response.meta.get('kw'), 'main': 'main'},
                callback=self.parse_type,
                dont_filter=True
            )
            if has_type:

                # for those name has type right after the name
                has_type_urls = has_type.css('li a::attr(href)')
                for has_type_url in has_type_urls:
                    yield scrapy.http.Request(
                        url=urlparse.urljoin(response.url, has_type_url.extract()),
                        meta={'kw': response.meta.get('kw'), 'main': 'notmain'},
                        callback=self.parse_type
                    )

    def parse_type(self, response):
        item = BaiduBaikeContentItem()
        self.logger.info('crawl {}'.format(response.meta.get('kw')))
        item['raw_kw'] = response.meta.get('kw')
        item['raw_kw_type'] = response.css('ul.polysemantList-wrapper li span::text').extract_first()
        item['raw_url'] = response.url
        item['raw_page_content'] = response.text
        item['raw_main'] = response.meta.get('main')

        # need change
        item['raw_type'] = u'人物'
        return item
