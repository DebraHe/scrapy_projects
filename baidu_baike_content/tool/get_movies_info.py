# -*- coding: utf-8 -*-

import json
import re
from scrapy.selector import Selector

RESULT_FILE = 'movies.json'


def merge():
    result = []
    with open(RESULT_FILE) as f:
        lines = f.readlines()
    for line in lines:
        try:
            d = {}

            page_content = json.loads(line.strip()).get(
                'download_data').get('raw_data').get('raw_page_content')   # 读取页面HTML
            kw = json.loads(line.strip()).get(
                'download_data').get('raw_data').get('raw_kw')  # 读取关键词
            url = json.loads(line.strip()).get(
                'download_data').get('raw_data').get('raw_url')  # 读取页面URL
            main = json.loads(line.strip()).get(
                'download_data').get('raw_data').get('raw_main')  # 读取页面是否为百度百科最匹配的搜索词条
            douban_id = json.loads(line.strip()).get(
                'download_data').get('raw_data').get('raw_douban_id')  # 读取豆瓣ID

            response = Selector(text=page_content)

            # 获取所有结构化数据

            dict_list = {}
            names_left = response.css('div.basic-info dl.basicInfo-left dt.name').extract()
            values_left = response.css('div.basic-info dl.basicInfo-left dd.value')
            for name_left, value_left in zip(names_left,values_left):
                dict_list[name_left.replace(u'\xa0', u'')] = value_left.xpath('string(.)').extract_first().strip()

            names_right = response.css('div.basic-info dl.basicInfo-right dt.name::text').extract()
            values_right = response.css('div.basic-info dl.basicInfo-right dd.value')
            for name_right, value_right in zip(names_right, values_right):
                dict_list[name_right.replace(u'\xa0', u'')] = value_right.xpath('string(.)').extract_first().strip()

            parsed_dict_one = {
                "name": "",
                "alternateName": "",
                "dateProducted": "",
                "productionCompany": "",
                "countryOfOrigin": "",
                "director": "",
                "creator": "",
                "genre": "",
                "actor": "",
                "durationInMinutes": "",
                "datePublished": "",
                "inLanguage": "",
                "color": "",
                "imdbId": "",
                "platform": "",
                "breadth": "",
                "mixing": "",
                "cost": "",
                "shotFilmFormat": "",
                "printedFilmFormat": ""
            }
            # 中文字段变英文字段

            if u'对白语言' in dict_list:
                parsed_dict_one['inLanguage'] = dict_list[u'对白语言']

            if u'出品时间' in dict_list:
                parsed_dict_one['dateProducted'] = dict_list[u'出品时间']

            if u'幅面' in dict_list:
                parsed_dict_one['breadth'] = dict_list[u'幅面']

            if u'中文名' in dict_list:
                parsed_dict_one['name'] = dict_list[u'中文名']

            if u'出品公司' in dict_list:
                parsed_dict_one['productionCompany'] = dict_list[u'出品公司']

            if u'制片地区' in dict_list:
                parsed_dict_one['countryOfOrigin'] = dict_list[u'制片地区']

            if u'imdb编码' in dict_list:
                parsed_dict_one['imdbId'] = dict_list[u'imdb编码']

            if u'洗印格式' in dict_list:
                parsed_dict_one['printedFilmFormat'] = dict_list[u'洗印格式']

            if u'制片人' in dict_list:
                parsed_dict_one['creator'] = dict_list[u'制片人']

            if u'摄制格式' in dict_list:
                parsed_dict_one['shotFilmFormat'] = dict_list[u'摄制格式']

            if u'片长' in dict_list:
                parsed_dict_one['durationInMinutes'] = dict_list[u'片长']

            if u'主演' in dict_list:
                parsed_dict_one['actor'] = dict_list[u'主演']

            if u'上映时间' in dict_list:
                parsed_dict_one['datePublished'] = dict_list[u'上映时间']

            if u'制片人' in dict_list:
                parsed_dict_one['director'] = dict_list[u'制片人']

            if u'色彩' in dict_list:
                parsed_dict_one['color'] = dict_list[u'色彩']

            if u'制作成本' in dict_list:
                parsed_dict_one['cost'] = dict_list[u'制作成本']

            if u'在线播放平台' in dict_list:
                parsed_dict_one['platform'] = dict_list[u'在线播放平台']

            if u'类型' in dict_list:
                parsed_dict_one['genre'] = dict_list[u'类型']

            if u'其它译名' in dict_list:
                parsed_dict_one['alternateName'] = dict_list[u'其它译名']

            if u'混音' in dict_list:
                parsed_dict_one['mixing'] = dict_list[u'混音']

            description = response.css('div.para').extract()
            roleName =response.css('li.listItem dl.info')

            # 职员表
            staffList = {}
            names_staffList = response.css('div#staffList tr td.list-key::text').extract()
            values_staffList = response.css('div#staffList tr td.list-value')
            for name, value in zip(names_staffList, values_staffList):
                staffList[name] = value.xpath('string(.)').extract_first().strip().replace(u'\xa0', u'')

            # 角色介绍
            parsed_list_two =[]

            role_descriptions = response.css('div.lemmaWgt-roleIntroduction li.roleIntroduction-item dl.roleIntrodcution-descritpion')
            for role_description in role_descriptions:
                parsed_dict_two = {
                    "roleName": "演员",
                    "@type": [
                        "PeformanceRole",
                        "Thing"
                    ],
                    "name": "",
                    "introduction": "",
                    "actor": {
                        "name": ""
                    },
                    "voiceActor": {
                        "name": ""
                    }
                }
                if role_description.css('div.role-name span.item-value').xpath('string(.)').extract_first():
                    parsed_dict_two['name'] = role_description.css('div.role-name span.item-value').xpath('string(.)').extract_first().strip().replace(u'\xa0', u'')
                if role_description.css('dd.role-description').xpath('string(.)').extract_first():
                    parsed_dict_two['introduction'] = role_description.css('dd.role-description').xpath('string(.)').extract_first().strip().replace(u'\xa0', u'')
                if role_description.css('div.role-actor span.item-value').xpath('string(.)').extract_first():
                    parsed_dict_two['actor']['name'] = role_description.css('div.role-actor span.item-value').xpath('string(.)').extract_first().strip().replace(u'\xa0', u'')
                if role_description.css('div.role-voice span.item-value').xpath('string(.)').extract_first():
                    parsed_dict_two['voiceActor']['name'] = role_description.css('div.role-voice span.item-value').xpath('string(.)').extract_first().strip().replace(u'\xa0', u'')
                parsed_list_two.append(parsed_dict_two)


            parsed_dict_three = {}
            parsed_dict_keys_three = response.css('div.main-content table.table-view')[2].css('tr th::text').extract()
            parsed_list_three = []
            for _ in range(0, len(response.css('div.main-content table.table-view')[2].css('tr').extract())-1):
                parsed_list_three.append([])

            one_rowspan = []
            one_name = []
            for item in response.css('div.main-content table.table-view')[2].css('tr td').extract():
                if "rowspan" in item.replace(u'\xa0', u''):
                    one_rowspan.append(re.search('rowspan=\"(.*?)\"', item.replace(u'\xa0', u'')))
                else:
                    one_rowspan.append("0")
                one_name.append()
            # tbl_keys = sel.xpath('//dl/dt/text()').extract()
            # tbl_contents = sel.xpath('//dl/dd').extract()
            # for i, k in enumerate(tbl_keys):
            #     k = ''.join(k.strip().split())
            #     s = re.sub(r'<.*?>', '', tbl_contents[i])
            #     s = ''.join(s.strip().split())
            #     d[k] = s
            # result.append(d)
        except:
            print 'Json parsing error: {}'.format(line)
            continue
    return result

if __name__ == '__main__':
    l = merge()
    for _ in l:
        for k, v in _.items():
            print '{}: {}'.format(k.encode('utf8'), v.encode('utf8'))
        print
