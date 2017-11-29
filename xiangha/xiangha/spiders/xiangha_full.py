# -*- coding: utf-8 -*-
import scrapy
from xiangha.items import XianghaShicaiItem
from scrapy.selector import Selector


_META_VERSION = 'v1.0'


class XianghaFullSpider(scrapy.Spider):
    name = "xiangha_full"
    result_dir = './result'
    meta_version = _META_VERSION
    custom_settings = {
        'ITEM_PIPELINES': {
            'xiangha.pipelines.XianghaPipeline': 300,
        },
        'AUTOTHROTTLE_ENABLED': True,
    }

    def start_requests(self):
        name_map = {
            'y-weiB1': "维生素B1",
            'y-weiB2': "维生素B2",
            'y-weiB6': "维生素B6",
            'y-weiB12': "维生素B12",
        }
        for i in ['y-weiB1', 'y-weiB2', 'y-weiB6', 'y-weiB12']:
            yield scrapy.Request(
                "https://www.xiangha.com/shicai/{}".format(i),
                meta={"name":name_map[i]},
                callback=self.parse_list
        )

    def parse_list(self, response):
        selector = Selector(response)
        shicai = XianghaShicaiItem()
        shicai["url"] = response.request.url
        shicai["food"] = []
        shicai["description"] = selector.xpath('//body//div[@id="info"]//text()').extract_first()
        shicai["name"] = response.meta.get("name")
        for item in selector.xpath('//dl[@id="yichi"]/dd/div[@class="list"]//li'):
            shicai_type = item.xpath('../../h4//text()').extract_first().split("/")
            effect = item.xpath('./p[@class="effect kw"]//text()').extract_first().split("/")
            amount = float(effect[0][:-2])
            total = float(effect[-1][:-1])
            shicai["food"].append({
                "outName": item.xpath('./p[@class="name"]//text()').extract_first(),
                "inName": shicai["name"],
                "label": u'每'+effect[-1],
                "amount": amount,
                "percent": amount/total/1000,
                "outImage": item.xpath('.//img//@data-src').extract_first(),
                "@type": "Relation",
                "unit": "微克",
                "shicai_type": shicai_type
            })
        yield shicai
