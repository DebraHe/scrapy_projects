# -*- coding: utf-8 -*-
import json

import math
import urlparse

import scrapy
from encvs.items import EncvsItem

_META_VERSION = 'v1.0'


class GZDTAllSpider(scrapy.Spider):
    name = 'gzdt_all'
    meta_version = _META_VERSION
    result_dir = './result'
    filename = 'gzdt.json'
    search_url = 'http://www.envsc.cn/filesort/PagedList/0/19/{}?page={}'
    custom_settings = {
        'DOWNLOAD_DELAY': 0,
        'ITEM_PIPELINES': {
            'encvs.pipelines.EncvsPipeline': 301
        },
        'AUTOTHROTTLE_ENABLED': False,
    }

    def start_requests(self):
        page = str(1)
        yield scrapy.http.Request(
            url=self.search_url.format(page, page),
            callback=self.parse_list
        )

    def parse_list(self, response):
        datas = json.loads(response.text)
        total = datas.get('total')
        for data in datas.get('rows'):
            ArticleId = str(data.get('ArticleId'))
            item = EncvsItem()
            item['title'] = data.get('Title')
            item['release_time'] = data.get('ReportDate')
            yield scrapy.http.Request(
                url='http://www.envsc.cn/details/index/' + ArticleId,
                callback=self.parse_detail,
                meta={'item': item}
            )
        for page in range(2, int(math.ceil(total / 12.0)) + 1):
            yield scrapy.http.Request(
                url=self.search_url.format(page, page),
                callback=self.parse_list
            )

    def parse_detail(self, response):
        item = response.meta.get('item')
        item['url'] = response.url
        enclosure = {}

        content = response.css('div.infcon').xpath('string(.)').extract_first()
        if response.css('div.infcon table'):
            enclosure['table'] = response.css('div.infcon table').extract()
            if content.find(u'附件：') != -1:
                content = content[:content.find(u'附件：')]
        try:
            source = response.css('div.right').xpath('string(.)').extract_first().replace(u'来源：', '')
        except:
            index_num = content.find(u'来源：')
            if index_num != -1:
                source = content[index_num+3:]
                if source.find(u'附件：') != -1:
                    source = source[:source.find(u'附件：')]
            else:
                source = u''

        item['source'] = source
        item['content'] = content
        enclosure['file'] = [urlparse.urljoin(response.url, href) for href in
                             response.css('div.filelist a::attr(href)').extract()] + \
                            [urlparse.urljoin(response.url, href) for href in
                             response.css('div.infcon a::attr(href)').extract() if href.endswith(u'.pdf') or href.endswith(u'.PDF') or href.endswith(u'.rar') or href.endswith(u'.zip')]
        item['enclosure'] = enclosure.copy()
        return item