# -*- coding: utf-8 -*-
import urlparse

import datetime
import scrapy

from chemall51.items import Chemall51Item
_META_VERSION = 'v1.0'


class BasicSpider(scrapy.Spider):
    name = 'chemall51_add'
    result_dir = './result'
    meta_version = _META_VERSION
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'ITEM_PIPELINES': {
            'chemall51.pipelines.MongoDBPipeline': 300,
        },
        'AUTOTHROTTLE_ENABLED': False,
    }

    def start_requests(self):
        yield scrapy.Request(
            url='http://www.51chemall.com/news_list/{}.do'.format(1)
        )

    def parse(self, response):
        for each_item in response.css('div.news_list a.fl_l'):
            title = each_item.css('div.news_list_right h4::text').extract_first()
            time = each_item.css('div.news_list_right span.fl_l::text').extract_first()
            if time.split()[0] == datetime.date.today().strftime("%Y/%m/%d"):
                yield scrapy.Request(
                    url='http://www.51chemall.com/' + each_item.css('a.fl_l::attr(href)').extract_first(),
                    callback=self.parse_content,
                    meta={'time': time, 'title': title}
                )
        next_page = response.xpath(u'//a[text()="下一页>"]/@href').extract_first()
        if next_page and next_page != 'javascript:void(0)':
            yield scrapy.Request(
                url='http://www.51chemall.com/' + next_page,
            )

    def parse_content(self, response):
        content = response.css('div.news_detail').xpath('string(.)').extract_first()
        content_split = content.split(u'来源：')
        item = Chemall51Item()
        item['datePublished'] = response.meta.get('time')
        item['headline'] = response.meta.get('title')
        item['articleBody'] = content_split[0]
        item['annex'] = [urlparse.urljoin(response.url, each_pic)for each_pic in response.css('div.news_detail img::attr(src)').extract()]
        if len(content_split) == 2:
            item['copyrightHolder'] = content_split[1]
        else:
            item['copyrightHolder'] = ''
        item['url'] = response.url
        yield item