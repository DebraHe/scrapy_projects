# -*- coding: utf-8 -*-

import re

import scrapy


_META_VERSION = 'v1.0'


class TycListSpider(scrapy.Spider):
    name = "tyc_list"
    result_dir = './result'
    meta_version = _META_VERSION
    driver = None
    flag = False
    custom_settings = {
        'DOWNLOAD_DELAY': 4,
        'ITEM_PIPELINES': {
            'tianyancha.pipelines.TianyanchaPipeline': 300,
        },
        'DOWNLOADER_MIDDLEWARES': {
            'tianyancha.webdriver_middleware.TycLoginMiddleware': 530,
            'tianyancha.webdriver_middleware.TycListMiddleware': 543,
            'tianyancha.middlewares.AbuyunProxyMiddleware': 100,
        },
        'AUTOTHROTTLE_ENABLED': False,
    }

    def start_requests(self):
        yield scrapy.Request('https://www.tianyancha.com/login', callback=self.parse_login, meta={'login': True})

    def parse_login(self, response):
        # print response.request.headers
        # print response.request.headers.proxy
        with open('doc/list_done.txt') as f:
            done = list(set([i.strip() for i in f.readlines()]))
        with open('doc/failed_kw.txt') as f:
            done += list(set([i.strip() for i in f.readlines()]))
        with open('doc/keywords1.txt') as f:
            kws = list(set([i.strip().replace('(','（').replace(')','）') for i in f.readlines()]))
        todo = [i for i in kws if i not in done]
        print len(kws), len(done), len(todo)
        for kw in todo:
            yield scrapy.http.Request(
                url='http://www.tianyancha.com/search?key={}'.format(kw),
                meta={'kw': kw}
            )

    def parse(self, response):

        # inspect_response(response, self)
        got = False
        # print response.text
        kw = response.meta.get('kw')
        container = response.css('div.search_result_container div.search_result_single')
        for sel in container:
            item = {}
            s = sel.css('div.search_right_item a span').xpath('string(.)').extract_first()
            item['kw'] = kw
            item['source_url'] = response.url
            item['name'] = re.sub(r'<.*?>', '', s)
            item['item_url'] = ''.join(sel.xpath('./div[@class="search_right_item"]/div/a/@href').extract())
            item['legal'] = ''.join(sel.xpath(
                './div[@class="search_right_item"]/div[@class="search_row_new pt20"]/div[1]/div[1]/a/text()').extract())
            item['capital'] = ''.join(sel.xpath(
                './div[@class="search_right_item"]/div[@class="search_row_new pt20"]/div[1]/div[2]/span/text()').extract())
            item['registration_date'] = ''.join(sel.xpath(
                './div[@class="search_right_item"]/div[@class="search_row_new pt20"]/div[1]/div[3]/span/text()').extract())
            item['status'] = ''.join(
                sel.xpath('./div[@class="search_right_item"]/div[1]/div[1]/text()').extract()).strip()
            item['province'] = ''.join(sel.xpath(
                './div[@class="search_right_item"]/div[@class="search_row_new pt20"]/div[1]/div[4]/span[1]/text()').extract()).strip()
            old_name = ''.join(sel.xpath('.//div[@class="add"]/span[3]//text()').extract()).strip()
            if kw == item['name'].encode('utf8') or kw == old_name.encode('utf-8'):
                yield item
                got = True
                with open('doc/list_done.txt','a') as f:
                    f.write(item['kw']+'\n')
                break
        if not got:
            with open('doc/failed_kw.txt','a') as f:
                f.write(kw+'\n')
            print len(container), kw
