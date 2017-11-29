# -*- coding: utf-8 -*-

import os
import urllib2

import scrapy

import time

import signal
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from tool.rk import RClient
from can_rk.items import CanRk_wenshu_Item
from tool.tool import get_code, get_code_shixin, get_phantomjs, get_img
from scrapy_redis.spiders import RedisSpider
_META_VERSION = 'v1.0'


class WenshuSpider(RedisSpider):
    name = 'wenshu_list'
    result_dir = './result'
    meta_version = _META_VERSION
    custom_settings = {
        'ITEM_PIPELINES': {
            'can_rk.pipelines.CanRk_wenshu_Pipeline': 300,
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
    #     url = '锡林浩特市给排水有限责任公司'
    #     word = '全文检索'
    #     yield scrapy.Request(
    #         url='http://wenshu.court.gov.cn/list/list/?sorttype=1&conditions=searchWord+QWJS+++{}:{}'.format(
    #             urllib2.quote(word.encode('utf-8')), urllib2.quote(url.encode('utf-8'))),
    #         meta={'kw': url}
    #     )

    def make_requests_from_url(self, url):
        # url = '锡林浩特市给排水有限责任公司'
        word = '全文检索'
        return scrapy.Request(
            url='http://wenshu.court.gov.cn/list/list/?sorttype=1&conditions=searchWord+QWJS+++{}:{}'.format(
            urllib2.quote(word.encode('utf-8')), urllib2.quote(url.encode('utf-8'))),
            meta={'kw': url}
        )

    def parse(self, response):
        self.log()
        kw = response.meta.get('kw')
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap["phantomjs.page.settings.resourceTimeout"] = 1000
        cap["phantomjs.page.settings.loadImages"] = True
        cap["phantomjs.page.settings.disk-cache"] = True
        cap[
            "phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
        phantomjs_path = '/home/ubuntu/phantomjs-2.1.1-linux-x86_64/bin/phantomjs'
        dr = webdriver.PhantomJS(phantomjs_path, desired_capabilities=cap)
        dr.get(response.url)
        dr.save_screenshot('screen.jpg')


        if dr.current_url == 'http://wenshu.court.gov.cn/waf_verify.htm':
            element = dr.find_element_by_id('Image1')
            dr.save_screenshot('screen.jpg')
            rc = RClient('ruyi1234', 'ruokuai9426', '85762', 'e871cc48477c4e11999c0ede9ee0719f')
            left = element.location['x']
            top = element.location['y']
            right = element.location['x'] + element.size['width']
            bottom = element.location['y'] + element.size['height']
            dr.save_screenshot('code.jpg')
            im = get_img(left, right, top, bottom)
            code = rc.rk_create(im, 2040)['Result']
            print 'code is {}'.format(code)

            dr.find_element_by_class_name('code-input').send_keys(code)
            dr.save_screenshot('screen.jpg')
            dr.find_element_by_class_name('code-btn').click()  # 1
            time.sleep(10)
            dr.save_screenshot('screen.jpg')
            os.remove('code.jpg')
        try:
            WebDriverWait(dr, 10).until(lambda the_driver: the_driver.find_element_by_class_name('dataItem').is_displayed())
            if dr.find_elements_by_class_name('DocIds'):
                with open('doc/succeed_name3.txt', 'a') as f:
                    f.write(kw + '\n')
                for _id in dr.find_elements_by_class_name('DocIds'):
                    item = CanRk_wenshu_Item()
                    split_list = _id.get_attribute("value").split('|')
                    if len(split_list) == 3:
                        item['id'] = split_list[0]
                        item['name'] = split_list[1]
                        item['time'] = split_list[2]

                    item['raw_data'] = dr.page_source
                    item['url'] = dr.current_url
                    item['kw'] = kw
                    yield item
                dr.service.process.send_signal(signal.SIGTERM)
                dr.quit()
            else:
                with open('doc/failed_name3.txt', 'a') as f:
                    f.write(kw + '\n')
                dr.service.process.send_signal(signal.SIGTERM)
                dr.quit()
        except:
            with open('doc/failed_name3.txt', 'a') as f:
                    f.write(kw + '\n')
            dr.service.process.send_signal(signal.SIGTERM)
            dr.quit()
