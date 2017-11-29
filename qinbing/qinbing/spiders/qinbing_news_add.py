# -*- coding: utf-8 -*-
import urlparse
import datetime
import scrapy
from qinbing.items import QinbingItem

_META_VERSION = 'v1.0'


class QinBingSpider(scrapy.Spider):
    name = 'qinbing_news_add'
    result_dir = './result'
    meta_version = _META_VERSION
    custom_settings = {
        'CONCURRENT_REQUESTS': 1,
        'ITEM_PIPELINES': {
            'qinbing.pipelines.Qinbing_news_MongoDBPipeline': 300,
        },
        'AUTOTHROTTLE_ENABLED': False,
    }

    def start_requests(self):
            page = 1
        # for page in range(1, 16):
            yield scrapy.Request(
                url='http://www.qinbing.cn/hangye/{}'.format(page),
                meta={'news_type': '行业资讯'},
            )
            yield scrapy.Request(
                url='http://www.qinbing.cn/huixun/{}'.format(page),
                meta={'news_type': '行业会讯'},
            )
            yield scrapy.Request(
                url='http://www.qinbing.cn/fagui/{}'.format(page),
                meta={'news_type': '法律法规'},
            )
            yield scrapy.Request(
                url='http://www.qinbing.cn/qitazixun/{}'.format(page),
                meta={'news_type': '行业新闻'},
            )
            yield scrapy.Request(
                url='http://www.qinbing.cn/qiye/{}'.format(page),
                meta={'news_type': '企业咨询'},
            )

    def parse(self, response):
        news_type = response.meta.get('news_type')
        for each_item in response.css('div.zx_left1 div.list0 div.list2 a.cb6'):
            time = each_item.xpath('../../div[@class="list3"]//text()').extract_first().strip()
            if time.split()[0] == datetime.date.today().strftime("%Y/%m/%d"):
                yield scrapy.Request(
                    url=urlparse.urljoin(response.url, each_item.css('a::attr(href)').extract_first()),
                    callback=self.parse_content,
                    meta={'time': time, 'news_type': news_type},
                )

    def parse_content(self, response):
        news_type = response.meta.get('news_type')
        datePublished = response.meta.get('time')
        headline = response.css('div.article0::text').extract_first().strip()
        articleBody = ''.join(response.xpath('//div[@id="pastingspan1"]//text()').extract())
        item = QinbingItem()
        item['datePublished'] = datePublished
        item['headline'] = headline
        item['articleBody'] = articleBody
        item['news_type'] = news_type
        item['url'] = response.url
        yield item