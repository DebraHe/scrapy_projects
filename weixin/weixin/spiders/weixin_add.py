# -*- coding: utf-8 -*-
import sys
import urllib

import os
import urlparse

import scrapy
import signal
from PIL import Image
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

from weixin.items import ArticleItem

from tool.rk import RClient
from tool.tool import get_phantomjs, get_proxy, get_img, get_today

reload(sys)
sys.setdefaultencoding('utf-8')


_META_VERSION = 'v1.0'


class WeixinSpider(scrapy.Spider):
    name = "weixin_add"
    result_dir = './result'
    meta_version = _META_VERSION
    custom_settings = {
        'DOWNLOAD_DELAY': 3,
        'DOWNLOADER_MIDDLEWARES': {
            'weixin.middlewares.AbuyunProxyMiddleware': 90,
        },
        'ITEM_PIPELINES': {
            'weixin.pipelines.MongoDBPipleline': 300,
        },
        'AUTOTHROTTLE_ENABLED': True,
    }

    def start_requests(self):
        url = 'http://weixin.sogou.com/weixin?'
        keywords = [
            '中国中医药杂志',
            '医药魔方数据',
            '医药观察家',
            '药材盈',
            '中国化工报',
            '赛柏蓝',
            'CHPC专业医药风控合规管理',
            'GuosenHealthcare',
            '东方比特健康网',
            '米内网',
            'E药经理人',
            '药素网',
            '机工情报',
            '中国糖业协会',
            '白糖第一线',
            '广西糖网',
            '云南糖网',
            '中华纸业传媒',
            '包装地带',
            'zhidianmijin168',
            '纸引未来网',
            '中国好包装网',
            '中国造纸杂志社',
            '卓创塑料',
            '卓创化工',
            '卓创资讯订阅号',

            '石油观察',
            '健识局',
            '化工707',
            '中国医药报',
            '微LINK化工',
            '有料化学',
            '陶瓷信息',
            '广州化工交易中心',
            '煤化工网',
            '天天化工网',
            'ICIS安迅思',
            '化工在线',
            '中国外加剂网',
            '斯尔邦石化',
            'ouryaoinfo',
        ]
        for keyword in keywords:
            para_data = {
                'type': '1',
                'query': keyword,
                'ie': 'utf8',
                's_from': 'input',
                '_sug_': 'n',
            }
            yield scrapy.Request(url=url + urllib.urlencode(para_data), meta={'kind': keyword})

    def parse(self, response):
        try:
            cap = webdriver.DesiredCapabilities.PHANTOMJS
            cap["phantomjs.page.settings.resourceTimeout"] = 1000
            cap["phantomjs.page.settings.loadImages"] = True
            cap["phantomjs.page.settings.disk-cache"] = True
            cap["phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"

            driver = webdriver.PhantomJS(executable_path=get_phantomjs(), service_args=get_proxy(), desired_capabilities=cap)
            rc = RClient('ruyi1234', 'ruokuai9426', '85762', 'e871cc48477c4e11999c0ede9ee0719f')
            driver.get(response.url)
            driver.save_screenshot('screen_main.jpg')
            try:
                while driver.find_element_by_id('seccodeImage'):
                    element = driver.find_element_by_id('seccodeImage')
                    left = element.location['x'] + 110
                    top = element.location['y']
                    right = left + element.size['width']
                    bottom = top + element.size['height']
                    driver.save_screenshot('code_1.jpg')
                    im = Image.open('code_1.jpg')
                    im = im.crop((left, top, right, bottom))
                    r, g, b, a = im.split()
                    im = Image.merge("RGB", (r, g, b))
                    im.save('code_1.jpg')
                    with open('code_1.jpg', 'rb') as f:
                        res = f.read()
                        os.remove('code_1.jpg')
                        code = rc.rk_create(res, 3060)['Result']

                    self.logger.info('code_1 is ' + code)
                    driver.find_element_by_id('seccodeInput').send_keys(code)
                    driver.find_element_by_id('submit').click()
                    try:
                        WebDriverWait(driver, 10).until(
                            lambda the_driver: the_driver.find_element_by_class_name('tit').is_displayed())
                        # time.sleep(10)
                    except:
                        continue
            except:
                self.logger.info('code_1 is done')
                url = driver.find_element_by_css_selector('p.tit a:nth-child(1)').get_attribute('href')
            driver.save_screenshot('screen_main.jpg')
            try:
                url = response.xpath(
                    '//p[@class="tit"]/a')[0].xpath('./@href').extract_first()
            except:
                pass
            driver.get(url)
            try:
                while driver.find_element_by_id('verify_img'):
                    element = driver.find_element_by_id('verify_img')
                    left = element.location['x']
                    top = element.location['y']
                    right = element.location['x'] + element.size['width']
                    bottom = element.location['y'] + element.size['height']
                    driver.save_screenshot('code_2.jpg')
                    im = get_img(left, right, top, bottom)
                    os.remove('code_2.jpg')
                    code = rc.rk_create(im, 2040)['Result']
                    self.logger.info('code_2 is ' + code)
                    driver.find_element_by_id('input').send_keys(code)
                    driver.find_element_by_id('bt').click()
                    try:
                        WebDriverWait(driver, 10).until(
                            lambda the_driver: the_driver.find_element_by_class_name('weui_media_bd').is_displayed())
                    except:
                        continue
            except:
                self.logger.info('code_2 is done')
            driver.save_screenshot('screen_main.jpg')
            for elem in driver.find_elements_by_xpath(
                    '//div[@class="weui_media_bd"]'):
                url = 'http://mp.weixin.qq.com' + \
                    elem.find_element_by_class_name(
                        'weui_media_title').get_attribute('hrefs')
                date = elem.find_element_by_class_name('weui_media_extra_info').text
                if date == get_today():
                    yield scrapy.Request(url=url, callback=self.parse_info, meta={'kind': response.meta.get('kind')})

            driver.service.process.send_signal(signal.SIGTERM)
            driver.quit()
        except:
            yield scrapy.Request(response.url, dont_filter=True)

    def parse_info(self, response):

        item = ArticleItem()
        try:
            author = response.css('div#meta_content em.rich_media_meta_text')[1].css('em::text').extract_first()
        except:
            author = response.meta.get('kind')
        item['author'] = author
        item['headline'] = response.xpath(
            '//h2[@class="rich_media_title"]/text()').extract_first().strip()
        item['articleBody'] = ''.join(response.xpath(
            '//div[@class="rich_media_content "]').xpath('string(.)').extract()).strip()
        item['articleBody'] = ''.join(item['articleBody'].split())
        item['datePublished'] = response.xpath(
            '//em[@id="post-date"]/text()').extract_first().strip()
        item['copyrightHolder'] = response.xpath(
            './/a[@id="post-user"]/text()').extract_first().strip()
        item['url'] = response.url
        item['kind'] = response.meta.get('kind')
        item['annex'] = [urlparse.urljoin(response.url, each_pic)for each_pic in response.css('div#js_content img::attr(data-src)').extract()]
        yield item
