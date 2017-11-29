# -*- coding: utf-8 -*-
import scrapy
import urllib2
import urlparse
from xiangha.items import SchemaItem
from tool.tool import get_uuid
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
_META_VERSION = 'v1.0'


class ShicaiSpider(scrapy.Spider):
    name = "shicai"
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
            url='https://www.xiangha.com/shicai',
        )

    def parse(self, response):
        blocks = response.css('div.rec_classify_con div.rec_classify_cell')

        for block in blocks:
            tag_type_big = block.css('h3 a::text').extract_first()
            shicais = block.css('ul')
            for shicai in shicais:
                shicai_names = shicai.css('li a::text').extract()
                shicai_urls = shicai.css('li a::attr(href)').extract()
                tag_type_small = shicai_names[0]
                for shicai_name, shicai_url in zip(shicai_names[1:-1], shicai_urls[1:-1]):
                    self.logger.info('crawl {}/{}/{}'.format(tag_type_big, tag_type_small, shicai_name))
                    yield scrapy.http.Request(
                        url=urlparse.urljoin(response.url, shicai_url),
                        meta={"tag_type_big": tag_type_big, "tag_type_small": tag_type_small,  "shicai_name": shicai_name},
                        callback=self.parse_list,
                    )

    def parse_list(self, response):
        block = response.css('div.ing_main')
        image = response.css('div.ing_name div.pic img::attr(src)').extract_first()
        name = block.css('div.ing_name div.ins h1::text').extract_first()
        self.logger.info('crawl {}'.format(name))

        alternateName = block.css('div.ing_name div.ins p::text').extract_first()
        if alternateName and alternateName.startswith(u'别名：'):
            alternateName = alternateName[3:]
            alternateName = alternateName.split('、')
        else:
            alternateName = []

        suitableAudience = [block.css('div.ing_name div.ins p.suit::text').extract_first()]
        if suitableAudience[0] and suitableAudience[0].startswith(u'：'):
            suitableAudience[0] = suitableAudience[0][1:]

        unsuitableAudience = [block.css('div.ing_name div.ins p.avoid::text').extract_first()]
        if unsuitableAudience[0] and unsuitableAudience[0].startswith(u'：'):
            unsuitableAudience[0] = unsuitableAudience[0][1:]

        detail_urls = block.css('div.list_tab a::attr(href)').extract()

        global calories
        global suitableProduct_list
        global unsuitableProduct_list
        global recipe_list
        global containsNutritionElement_list

        for detail_url in detail_urls:
            if 'caipu' in detail_url:
                page_content1 = self.get_page(detail_url)
                page_response1 = scrapy.Selector(text=page_content1)
                recipe_list = []
                recipes = page_response1.css('div.ing_main div.rec_list ul li')
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
                    recipe_dict['image'] = recipe.css('a.pic img::attr(src)').extract_first()
                    recipe_dict['url'] = recipe.css('p.name a::attr(href)').extract_first()
                    if recipe.css('p.name a::attr(href)').re('caipu/(.*?)\.html'):
                        recipe_dict['identifier'] = recipe.css('p.name a::attr(href)').re('caipu/(.*?)\.html')[0]
                    if recipe_dict['name']:
                        recipe_dict['@id'] = get_uuid(recipe_dict['@type'], recipe_dict['name'])
                        recipe_list.append(recipe_dict)
            elif 'shicai' in detail_url:
                page_content2 = self.get_page(detail_url)
                page_response2 = scrapy.Selector(text=page_content2)
                description = page_response2.css('div.ing_main div.ing_con div.ing_ins h2#jianjie + p').xpath(
                    'string(.)').extract_first()
                healthEffects = [page_response2.css('div.ing_main div.ing_con div.ing_ins h2#gongxiao + p').xpath(
                    'string(.)').extract_first()]
                nutritionValue = [page_response2.css('div.ing_main div.ing_con div.ing_ins h2#yingying + p').xpath(
                    'string(.)').extract_first()]
                buyingInstruction = [page_response2.css('div.ing_main div.ing_con div.ing_ins h2#xuangou + p').xpath(
                    'string(.)').extract_first()]
                storageInstruction = [page_response2.css('div.ing_main div.ing_con div.ing_ins h2#cunchu + p').xpath(
                    'string(.)').extract_first()]
                eatingInstruction = [page_response2.css('div.ing_main div.ing_con div.ing_ins h2#jiqiao + p').xpath(
                    'string(.)').extract_first()]

                containsNutritionElements = page_response2.css('ul#eleInfo li')

                containsNutritionElement_list = []
                if containsNutritionElements:
                    calories = containsNutritionElements[0].css(
                        'em::text').extract_first()
                for containsNutritionElement in containsNutritionElements:
                    containsNutritionElement_dict = {
                        "out": {
                            "@id": "",
                            "@type": "NutritionElement",
                            "name": ""
                        },
                        "@id": "",
                        "@type": "BinaryRelationOut",
                        "value": "",
                        "unitText": ""
                    }
                    containsNutritionElement_dict["out"]["name"] = containsNutritionElement.css(
                        'span a::text').extract_first()
                    containsNutritionElement_dict["value"] = containsNutritionElement.css(
                        'em::text').extract_first()
                    containsNutritionElement_dict["unitText"] = containsNutritionElement.css(
                        'span::text').extract_first()[1:-1]
                    containsNutritionElement_dict['@id'] = get_uuid(
                        containsNutritionElement_dict['@type'],
                        containsNutritionElement_dict['value'])
                    containsNutritionElement_dict["out"]['@id'] = get_uuid(
                        containsNutritionElement_dict["out"]['@type'],
                        containsNutritionElement_dict["out"]['name'])
                    containsNutritionElement_list.append(containsNutritionElement_dict)

            elif 'xiangke' in detail_url:
                page_content3 = self.get_page(detail_url)
                page_response3 = scrapy.Selector(text=page_content3)
                products = page_response3.css('div.ing_main div.ing_tips td')
                yida_num = page_response3.css('th#yida::attr(rowspan)').extract_first()
                xiangke_num = page_response3.css('th#xiangke::attr(rowspan)').extract_first()
                if not yida_num:
                    yida_num = 0
                else:
                    yida_num = int(yida_num)

                if not xiangke_num:
                    xiangke_num = 0
                else:
                    xiangke_num =int(xiangke_num)
                suitableProduct_list = []
                unsuitableProduct_list = []
                if xiangke_num != 0:
                    for product in products[0:xiangke_num]:
                        unsuitableProduct_dict = {
                            "out": {
                                "@id": "",
                                "@type": "FoodIngredient",
                                "name": "",
                                "image": "",
                            },
                            "reason": "",
                            "@id": "",
                            "@type": "BinaryRelationOut"
                        }
                        unsuitableProduct_dict["out"]["name"] = product.css('::text').extract()[2].replace('：', '')
                        unsuitableProduct_dict["reason"] = product.css('a::text').extract_first()
                        if '：' not in product.css('::text').extract()[2]:
                            unsuitableProduct_dict["reason"] = product.css('a::text').extract()[1]
                            unsuitableProduct_dict["out"]['image'] = self.get_shicai_image(product.css('a::attr(href)').extract_first())
                        unsuitableProduct_dict['@id'] = get_uuid(
                            unsuitableProduct_dict['@type'],
                            unsuitableProduct_dict['reason'])
                        unsuitableProduct_dict["out"]['@id'] = get_uuid(
                            unsuitableProduct_dict["out"]['@type'],
                            unsuitableProduct_dict["out"]['name'])

                        unsuitableProduct_list.append(unsuitableProduct_dict)
                if yida_num != 0:
                    for product in products[xiangke_num:xiangke_num+yida_num]:
                        suitableProduct_dict = {
                            "out": {
                                "@id": "",
                                "@type": "FoodIngredient",
                                "name": "",
                                "image":"",
                            },
                            "reason": "",
                            "@id": "",
                            "@type": "BinaryRelationOut"
                        }
                        suitableProduct_dict["out"]["name"] = product.css('::text').extract()[2].replace('：', '')
                        suitableProduct_dict["reason"] = product.css('a::text').extract_first()
                        if '：' not in product.css('::text').extract()[2]:
                            suitableProduct_dict["reason"] = product.css('a::text').extract()[1]
                            suitableProduct_dict["out"]['image'] = self.get_shicai_image(product.css('a::attr(href)').extract_first())
                        suitableProduct_dict['@id'] = get_uuid(
                            suitableProduct_dict['@type'],
                            suitableProduct_dict['reason'])
                        suitableProduct_dict["out"]['@id'] = get_uuid(
                            suitableProduct_dict["out"]['@type'],
                            suitableProduct_dict["out"]['name'])

                        suitableProduct_list.append(suitableProduct_dict)

        item = SchemaItem()
        item['url'] = response.url
        tag = [{
            "name": response.meta.get('tag_type_big'),
            "@id": get_uuid("Tag", response.meta.get('tag_type_big')),
            "@type": ["Tag", "Thing"],
            "category":"taxonomy"
        },{
            "name": response.meta.get('tag_type_small'),
            "@id": get_uuid("Tag", response.meta.get('tag_type_small')),
            "@type": ["Tag", "Thing"],
            "category":"taxonomy"}
        ]
        schema = {
            "statedIn": "www.xiangha.com",
            "referenceUrl": response.url,
            "@id": get_uuid("FoodIngredient", name),
            "@type": ["FoodIngredient", "Thing"],
            "name": name,
            "description": description,
            "alternateName": alternateName,
            "image": image,
            "nutritionValue": nutritionValue,
            "healthEffects": healthEffects,
            "eatingInstruction": eatingInstruction,
            "storageInstruction": storageInstruction,
            "buyingInstruction": buyingInstruction,
            "suitableAudience": suitableAudience,
            "unsuitableAudience": unsuitableAudience,
            "containsNutritionElement": containsNutritionElement_list,
            "calories": calories,
            "recipe": recipe_list,
            "suitableProduct": suitableProduct_list,
            "unsuitableProduct": unsuitableProduct_list,
            "tag": tag,

        }
        item['schema'] = schema
        return item

    def get_page(self, url):
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        headers = {'User-Agent': user_agent}
        request = urllib2.Request(url=url, headers=headers)
        response = urllib2.urlopen(request)
        page = response.read()
        return page

    def get_shicai_image(self, url):
        page_content = self.get_page(url)
        page_response = scrapy.Selector(text=page_content)
        return page_response.css('div.ing_name div.pic img::attr(src)').extract_first()