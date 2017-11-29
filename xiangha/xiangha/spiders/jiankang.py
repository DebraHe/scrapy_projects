# -*- coding: utf-8 -*-
import re

import scrapy
import urlparse
from xiangha.items import SchemaItem
from tool.tool import get_uuid
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
_META_VERSION = 'v1.0'


class JiankangSpider(scrapy.Spider):
    name = "jiankang"
    result_dir = './result'
    meta_version = _META_VERSION
    custom_settings = {
        'ITEM_PIPELINES': {
            'xiangha.pipelines.SchemaPipeline': 300,
        },
        'AUTOTHROTTLE_ENABLED': True,
    }

    def start_requests(self):
        yield scrapy.http.Request(
            url='https://www.xiangha.com/jiankang',
        )

    def parse(self, response):
        blocks = response.css('div.rec_classify_con div.rec_classify_cell div.rec_classify_cell')
        for block in blocks[0:4]:
            tag_type_big = block.css('h3::text').extract_first()
            jiankangs = block.css('ul')
            for jiankang in jiankangs:
                jiankang_names = jiankang.css('li a::text').extract()
                jiankang_urls = jiankang.css('li a::attr(href)').extract()
                for jiankang_name, jiankang_url in zip(jiankang_names[1:-1], jiankang_urls[1:-1]):
                    self.logger.info('crawl {}/{}'.format(tag_type_big, jiankang_name))
                    yield scrapy.http.Request(
                        url=urlparse.urljoin(response.url, jiankang_url),
                        meta={"tag_type_big": tag_type_big,  "jiankang_name": jiankang_name},
                        callback=self.parse_list,
                    )
        for block in blocks[7:]:
            tag_type_big = block.css('h3::text').extract_first()
            jiankangs = block.css('ul')
            for jiankang in jiankangs:
                jiankang_names = jiankang.css('li a::text').extract()
                jiankang_urls = jiankang.css('li a::attr(href)').extract()
                for jiankang_name, jiankang_url in zip(jiankang_names[1:-1], jiankang_urls[1:-1]):
                    self.logger.info('crawl {}/{}'.format(tag_type_big, jiankang_name))
                    yield scrapy.http.Request(
                        url=urlparse.urljoin(response.url, jiankang_url),
                        meta={"tag_type_big": tag_type_big,  "jiankang_name": jiankang_name},
                        callback=self.parse_list,
                    )
        for block in blocks[4:7]:
            tag_type_big = block.css('h3::text').extract_first()
            jiankangs = block.css('ul')
            for jiankang in jiankangs:
                jiankang_names = jiankang.css('li a::text').extract()
                jiankang_urls = jiankang.css('li a::attr(href)').extract()
                for jiankang_name, jiankang_url in zip(jiankang_names[1:-1], jiankang_urls[1:-1]):
                    self.logger.info('crawl {}/{}'.format(tag_type_big, jiankang_name))
                    yield scrapy.http.Request(
                        url=urlparse.urljoin(response.url, jiankang_url),
                        meta={"tag_type_big": tag_type_big,  "jiankang_name": jiankang_name},
                        callback=self.parse_detail_rich,
                    )

    def parse_list(self, response):
        description = response.css('div#infoHide::text').extract()
        if description:
            description = '\n'.join([m.strip() for m in response.css('div#infoHide::text').extract()])
        else:
            description = '\n'.join([m.strip() for m in response.css('div#info::text').extract()])
        unsuitableProductInstruction = response.css('dl#jichi div.eat_ins p::text').extract_first()
        suitableProductInstruction = response.css('dl#yichi div.eat_ins p::text').extract_first()
        name = response.meta.get('jiankang_name')

        suitableProduct_list = []
        unsuitableProduct_list = []
        yichi_lists = response.css('dl#yichi div.list li')
        for yichi_list in yichi_lists:
            yichi_dict = {
                "reason": "",
                "@id": "",
                "@type": "BinaryRelationOut",
                "out": {
                    "image": "",
                    "@id": "",
                    "@type": "FoodIngredient",
                    "name": ""
                },
                "tag": [{
                    "name": "",
                    "@id": "",
                    "@type": ["Tag", "Thing"],
                    "category": "taxonomy"
                }]
            }
            yichi_dict["tag"][0]["name"] = yichi_list.xpath('../../h4//text()').extract_first()
            yichi_dict["tag"][0]["@id"] = get_uuid("Tag", yichi_dict["tag"][0]["name"])
            yichi_dict["reason"] = yichi_list.css('p.effect::text').extract_first()
            yichi_dict["out"]["image"] = yichi_list.css('img::attr(data-src)').extract_first()
            yichi_dict["out"]["name"] = yichi_list.css('p.name a::text').extract_first()
            if yichi_dict["reason"]:
                yichi_dict["@id"] = get_uuid(yichi_dict["@type"], yichi_dict["reason"])
            yichi_dict["out"]["@id"] = get_uuid(yichi_dict["out"]["@type"], yichi_dict["out"]["name"])
            suitableProduct_list.append(yichi_dict)

        jichi_lists = response.css('dl#jichi div.list li')
        for jichi_list in jichi_lists:
            jichi_dict = {
                "reason": "",
                "@id": "",
                "@type": "BinaryRelationOut",
                "out": {
                    "image": "",
                    "@id": "",
                    "@type": "FoodIngredient",
                    "name": ""
                },
                "tag": [{
                    "name": "",
                    "@id": "",
                    "@type": ["Tag", "Thing"],
                    "category": "taxonomy"
                }]
            }
            jichi_dict["tag"][0]["name"] = jichi_list.xpath('../../h4//text()').extract_first()
            jichi_dict["tag"][0]["@id"] = get_uuid("Tag", jichi_dict["tag"][0]["name"])
            jichi_dict["reason"] = jichi_list.css('p.effect::text').extract_first()
            jichi_dict["out"]["image"] = jichi_list.css('img::attr(data-src)').extract_first()
            jichi_dict["out"]["name"] = jichi_list.css('p.name a::text').extract_first()
            if jichi_dict["reason"]:
                jichi_dict["@id"] = get_uuid(jichi_dict["@type"], jichi_dict["reason"])
            jichi_dict["out"]["@id"] = get_uuid(jichi_dict["out"]["@type"], jichi_dict["out"]["name"])
            unsuitableProduct_list.append(jichi_dict)

        item = SchemaItem()
        item['url'] = response.url

        schema = {
            "unsuitableProductInstruction": unsuitableProductInstruction,
            "suitableProductInstruction": suitableProductInstruction,
            "@id": get_uuid("FoodIngredient", name),
            "@type": ["FoodIngredient", "Thing"],
            "name": name,
            "description": description,
            "recipe": [],
            "suitableProduct": suitableProduct_list,
            "unsuitableProduct": unsuitableProduct_list,

        }
        item['schema'] = schema

        recipe_url = response.url + '-1'
        yield scrapy.http.Request(
            url=recipe_url,
            meta={
                'item': item.copy()
            },
            callback=self.parse_detail
        )

    def parse_detail(self, response):
        item = response.meta.get('item')
        recipe_list = []
        recipes = response.css('div.hea_main div.rec_list ul li')
        for recipe in recipes:
            recipe_dict = {
                "@id": "",
                "@type": "Recipe",
                "identifier": "",
                "name": "",
                "image": "",
                "url": ""
            }
            recipe_dict['name'] = recipe.css('p.name a::text').extract_first()
            recipe_dict['image'] = recipe.css('img::attr(data-src)').extract_first()
            recipe_dict['url'] = recipe.css('p.name a::attr(href)').extract_first()
            if recipe.css('p.name a::attr(href)').re('caipu/(.*?)\.html'):
                recipe_dict['identifier'] = recipe.css('p.name a::attr(href)').re('caipu/(.*?)\.html')[0]
            if recipe_dict['name']:
                recipe_dict['@id'] = get_uuid(recipe_dict['@type'], recipe_dict['name'])
                recipe_list.append(recipe_dict)
        item['schema']['recipe'] = recipe_list
        return item

    def parse_detail_rich(self, response):
        description = response.css('div#infoHide::text').extract()
        if description:
            description = '\n'.join([m.strip() for m in response.css('div#infoHide::text').extract()])
        else:
            description = '\n'.join([m.strip() for m in response.css('div#info::text').extract()])
        name = response.meta.get('jiankang_name')
        isRichIn_list = []
        for item in response.xpath('//dl[@id="yichi"]/dd/div[@class="list"]//li'):
            shicai_type = item.xpath('../../h4//text()').extract_first()
            shicai_effect = item.xpath('./p[@class="effect kw"]//text()').extract_first().split("/")[0]
            shicai_name = item.xpath('./p[@class="name"]//text()').extract_first()
            shicai_image = item.xpath('.//img//@data-src').extract_first()
            isRichIn_list.append({
                "out": {
                    "image": shicai_image,
                    "@id": get_uuid("FoodIngredient", shicai_name),
                    "@type": "FoodIngredient",
                    "name": shicai_name
                },
                "@id": get_uuid("BinaryRelationOut", shicai_name),
                "@type": "BinaryRelationOut",
                "value": re.search('([\d\.]+)', shicai_effect).group(1),
                "unitText": re.search('([^\d\.]+)', shicai_effect).group(1),
                "tag": [{
                    "name": shicai_type,
                    "@id": get_uuid("Tag", shicai_type),
                    "@type": ["Tag", "Thing"],
                    "category": "taxonomy"
                }]
            })

        item = SchemaItem()
        item['url'] = response.url

        schema = {
            "@id": get_uuid("FoodIngredient", name),
            "@type": ["FoodIngredient", "Thing"],
            "name": name,
            "description": description,
            "isRichIn": isRichIn_list,

        }
        item['schema'] = schema
        return item


