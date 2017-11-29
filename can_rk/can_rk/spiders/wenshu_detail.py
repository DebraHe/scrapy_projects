# -*- coding: utf-8 -*-

import os

import re
import scrapy

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from tool.rk import RClient
from can_rk.items import CanRk_wenshu_Item
from tool.tool import get_code, get_code_shixin, get_phantomjs, get_img
from scrapy_redis.spiders import RedisSpider
_META_VERSION = 'v1.0'


class WenshuSpider(RedisSpider):
# class WenshuSpider(scrapy.Spider):
    name = 'wenshu_detail'
    result_dir = './result'
    meta_version = _META_VERSION
    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'ITEM_PIPELINES': {
            'can_rk.pipelines.CanRk_wenshu_detail_Pipeline': 300,
        },
        'AUTOTHROTTLE_ENABLED': False,
    }
    user_agents = [
        'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
        'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
        'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
        'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
        'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
        'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
        'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11'
    ]

    # def start_requests(self):
    #     with open('doc/code_failed4.txt') as f:
    #         for line in f.readlines():
    #             yield scrapy.Request(
    #                 url='http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID={}'.format(line.strip()),
    #                 meta={'kw': line.strip()}
    #             )

    def make_requests_from_url(self, url):
        return scrapy.Request(
            url='http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID={}'.format(url),
            meta={'kw': url}
        )

    def parse(self, response):
        kw = response.meta.get('kw')
        if 'VisitRemind.html?' in response.text:
            cap = webdriver.DesiredCapabilities.PHANTOMJS
            cap["phantomjs.page.settings.resourceTimeout"] = 1000
            cap["phantomjs.page.settings.loadImages"] = True
            cap["phantomjs.page.settings.disk-cache"] = True
            cap[
                "phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
            phantomjs_path = '/home/ubuntu/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'
            dr = webdriver.PhantomJS(phantomjs_path, desired_capabilities=cap)
            dr.get('http://wenshu.court.gov.cn/Html_Pages/VisitRemind.html?DocID=' + kw)

            element = dr.find_element_by_name('validateCode')
            rc = RClient('ruyi1234', 'ruokuai9426', '85762', 'e871cc48477c4e11999c0ede9ee0719f')
            left = element.location['x']
            top = element.location['y']
            right = element.location['x'] + element.size['width']
            bottom = element.location['y'] + element.size['height']
            dr.save_screenshot('code.jpg')
            im = get_img(left, right, top, bottom)
            code = rc.rk_create(im, 1040)['Result']
            print 'code is {}'.format(code)

            dr.find_element_by_id('txtValidateCode').send_keys(code)
            dr.find_element_by_class_name('btn_validatecode').click()
            WebDriverWait(dr, 10).until(
                lambda the_driver: the_driver.find_element_by_class_name('head_search_key').is_displayed())
            os.remove('code.jpg')
            yield scrapy.Request(
                url='http://wenshu.court.gov.cn/CreateContentJS/CreateContentJS.aspx?DocID={}'.format(kw),
                meta={'kw': kw},
                dont_filter=True
            )
        else:
            item = CanRk_wenshu_Item()
            try:
                item['content'] = re.search(ur'\\"Html\\":\\"(.*?)\\"}";', response.xpath('string(.)').extract_first()).group(1)
            except:
                item['content'] = re.search(ur'\\"Html\\":\\"(.*)', response.xpath('string(.)').extract_first()).group(1)
            item['raw_data'] = response.text
            item['url'] = response.url
            item['id'] = kw
            yield item
