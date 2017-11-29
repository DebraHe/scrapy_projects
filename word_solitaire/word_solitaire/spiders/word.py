# -*- coding: utf-8 -*-
"""
反爬：无

爬取策略：遍历沪江网上所有词语，在中华诗词网上查找相关拼音，由于数量庞大，服务器采用Redis做存储下载并上传s3。

"""
import codecs

import scrapy
import urlparse
from word_solitaire.items import WordSolitaireItem
from tool.tool import cht_to_chs

import sys
reload(sys)
sys.setdefaultencoding('utf8')

_META_VERSION = 'v1.0'


class WordSpider(scrapy.Spider):
    name = "word"
    result_dir = './result'
    meta_version = _META_VERSION
    custom_settings = {
        'ITEM_PIPELINES': {
            'word_solitaire.pipelines.WordSolitairePipeline': 300,
        },
        'AUTOTHROTTLE_ENABLED': True,
    }

    def start_requests(self):
        yield scrapy.Request(url="https://www.hujiang.com/cidian/cdzxcx_1/", callback=self.parse_list)

    def parse_list(self, response):
        hujiangs = response.css("div.in_list_conent>ul>li")
        for hujiang in hujiangs:
            word = hujiang.css("a::text").extract_first()

            over = {}
            with codecs.open('doc/done.txt', 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    over[line.strip()] = 1

            if word.strip() in over.keys():
                continue

            pinyin_url = 'http://www.zdic.net/sousuo/'

            post_data = {
                "lb_a": "hp",
                "lb_b": "mh",
                "lb_c": "mh",
                "tp": "tp1",
                "q": word,
            }

            yield scrapy.FormRequest(
                url=pinyin_url,
                meta={'word': word},
                formdata=post_data,
                callback=self.parse_detail)

        # next page
        next_page = response.css('div#ContentPlaceHolder1_subContentPlaceHolder1_paging_split_page a:last-child')
        if next_page.css('::text').extract_first() == u'下一页 >':
            next_page_url = urlparse.urljoin(response.url, next_page.css('::attr(href)').extract_first())
            yield scrapy.Request(next_page_url, callback=self.parse_list)

    def parse_detail(self, response):
        item = WordSolitaireItem()
        item['word'] = response.meta.get('word')
        item['url'] = response.url
        pinyin = response.css('div#ciif span.dicpy::text').extract_first()
        if pinyin:
            item['pinyin'] = pinyin.strip()
        else:
            item['pinyin'] = pinyin

        expression = response.xpath('//*[@id="cd"]//span[@class="diczx4"]/../text()').extract()
        if expression:
            item['expression'] = ''.join(expression)
        else:
            expression = response.css('div.gycd-item:nth-child(1)>li>p.def>span.gc_sy::text').extract_first()
            if expression:
                item['expression'] = cht_to_chs(expression)
            else:
                item['expression'] = expression
        return item

