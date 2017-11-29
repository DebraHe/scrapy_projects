# -*- coding: utf-8 -*-
"""
反爬：无

爬取策略：抓取网页数据，下载并上传s3。

"""
import scrapy
import urlparse
from dao18.items import Dao18Item

_META_VERSION = 'v1.0'


class ContentSpider(scrapy.Spider):
    name = "content"
    result_dir = './result'
    meta_version = _META_VERSION
    custom_settings = {
        'ITEM_PIPELINES': {
            'dao18.pipelines.Dao18Pipeline': 300,
        },
        'AUTOTHROTTLE_ENABLED': True,
    }

    def start_requests(self):
        name_url_items = [
            {
                'name_category': u'中国古代作者',
                'name_url': 'https://cn.18dao.net/%E5%90%8D%E4%BA%BA%E5%90%8D%E8%A8%80/%E4%B8%AD%E5%9B%BD%E5%8F%A4%E4%BB%A3%E4%BD%9C%E8%80%85',
            },
            {
                'name_category': u'中国近代作者',
                'name_url': 'https://cn.18dao.net/%E5%90%8D%E4%BA%BA%E5%90%8D%E8%A8%80/%E4%B8%AD%E5%9B%BD%E8%BF%91%E4%BB%A3%E4%BD%9C%E8%80%85',
            },
            {
                'name_category': u'各国谚语',
                'name_url': 'https://cn.18dao.net/%E5%90%8D%E4%BA%BA%E5%90%8D%E8%A8%80/%E5%90%84%E5%9B%BD%E8%B0%9A%E8%AF%AD',
            },
            {
                'name_category': u'外国作者',
                'name_url': 'https://cn.18dao.net/%E5%90%8D%E4%BA%BA%E5%90%8D%E8%A8%80/%E5%A4%96%E5%9B%BD%E4%BD%9C%E8%80%85',
            },
            {
                'name_category': u'书摘名言',
                'name_url': 'https://cn.18dao.net/%E5%90%8D%E4%BA%BA%E5%90%8D%E8%A8%80/%E4%B9%A6%E6%91%98%E5%90%8D%E8%A8%80',
            },
            {
                'name_category': u'其他作者',
                'name_url': 'https://cn.18dao.net/%E5%90%8D%E4%BA%BA%E5%90%8D%E8%A8%80/%E5%85%B6%E4%BB%96%E4%BD%9C%E8%80%85',
            },
        ]
        for name_url_item in name_url_items:
            yield scrapy.http.Request(
                url=name_url_item['name_url'],
                meta={'name_category': name_url_item['name_category']}
            )

    def parse(self, response):
        name_category = response.meta.get('name_category')
        for a_item in response.xpath('//table[@width="100%"]//td/a'):
            name = a_item.css('a::text').extract_first()
            url = a_item.css('a::attr(href)').extract_first()
            yield scrapy.http.Request(
                url=urlparse.urljoin(response.url, url),
                meta={
                    'name_category': name_category,
                    'name': name.strip()
                },
                callback=self.parse_detail
            )

    def parse_detail(self, response):
        item = Dao18Item()
        item['name_category'] = response.meta.get('name_category')
        item['name'] = response.meta.get('name')
        item['url'] = response.url
        content_list = []
        for content_items in response.css('ol li'):
            content_item = content_items.xpath('string(.)').extract_first().split(u'类别:')
            if len(content_item) == 2:
                content_dict = {
                    'content': content_item[0].strip(),
                    'content_category': content_item[1].strip()
                }
                content_list.append(content_dict)
        item['content_list'] = content_list[:]
        return item
