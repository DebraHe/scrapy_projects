# -*- coding: utf-8 -*-
import urlparse


import datetime
import scrapy

import signal
from selenium import webdriver

from gov_cn.items import GovCnItem

_META_VERSION = 'v1.0'


class GovCnSpider(scrapy.Spider):
    name = 'falvfagui_add'
    result_dir = './result'
    filename = name + '.json'
    meta_version = _META_VERSION
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'ITEM_PIPELINES': {
            'gov_cn.pipelines.MongoDBPipeline': 300,
        },
        'AUTOTHROTTLE_ENABLED': False,
    }

    def start_requests(self):
        page = 1
        yield scrapy.Request(
            url='http://www.chinalaw.gov.cn/col/col11/index.html?uid=1648&pageNum={}'.format(page),
            meta={'Bigtype': '政策_法律法规'}
        )
        yield scrapy.Request(
            url='http://www.chinalaw.gov.cn/col/col12/index.html?uid=1648&pageNum={}'.format(page),
            meta={'Bigtype': '政策_法律法规'}
        )
        yield scrapy.Request(
            url='http://www.chinalaw.gov.cn/col/col13/index.html?uid=1648&pageNum={}'.format(page),
            meta={'Bigtype': '政策_法律法规'}
        )
        yield scrapy.Request(
            url='http://www.chinalaw.gov.cn/col/col14/index.html?uid=1648&pageNum={}'.format(page),
            meta={'Bigtype': '政策_法律法规'}
        )
        yield scrapy.Request(
            url='http://www.chinalaw.gov.cn/col/col15/index.html?uid=1648&pageNum={}'.format(page),
            meta={'Bigtype': '政策_法律法规'}
        )

    def parse(self, response):
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap["phantomjs.page.settings.resourceTimeout"] = 1000
        cap["phantomjs.page.settings.loadImages"] = True
        cap["phantomjs.page.settings.disk-cache"] = True
        cap[
            "phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
        phantomjs_path = '/home/ubuntu/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'
        # phantomjs_path = '/Users/debrahe/Desktop/phantomjs-2.1.1-macosx/bin/phantomjs'
        dr = webdriver.PhantomJS(phantomjs_path, desired_capabilities=cap)
        dr.get(response.url)
        sel = scrapy.Selector(text=dr.page_source)
        for each_item in sel.css('ul.lmlb li'):
            title = each_item.css('a::text').extract_first()
            time = each_item.css('span::text').extract_first()
            if time == datetime.date.today().strftime("%Y-%m-%d"):
                yield scrapy.Request(
                    url='http://www.chinalaw.gov.cn' + each_item.css('a::attr(href)').extract_first(),
                    callback=self.parse_content,
                    meta={'time': time, 'title': title, 'Bigtype': response.meta.get('Bigtype')}
                )
        dr.service.process.send_signal(signal.SIGTERM)
        dr.quit()

    def parse_content(self, response):
        item = GovCnItem()
        item['datePublished'] = response.meta.get('time').strip()
        item['headline'] = response.meta.get('title')
        item['Bigtype'] = response.meta.get('Bigtype')
        item['articleBody'] = response.css('div#zoom').xpath('string(.)').extract_first()
        item['annex'] = [urlparse.urljoin(response.url, each_pic) for each_pic in
                         response.css('div#zoom img::attr(src)').extract()]
        try:
            item['copyrightHolder'] = response.css('span.sp_time font:nth-child(2)::text').extract_first().split(u'：')[
                1].strip()
        except:
            item['copyrightHolder'] = ''
        item['url'] = response.url

        yield item