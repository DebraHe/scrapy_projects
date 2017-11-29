# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import pymongo


from tool.tool import unicode_to_str
from heweather.items import BasicItem
import json


class HeweatherPipeline(object):
    def process_item(self, item, spider):
        filename = spider.filename
        result_dir = spider.result_dir
        result = {
            'meta_version': spider.meta_version,
            'meta_updated': datetime.datetime.now().isoformat()[:19],
            'download_config': {
                'url': '',
                'method': 'GET',
            },
            'download_data': {
                'parsed_data': {},
                'raw_data': {},
            }
        }
        result['download_config']['url'] = unicode_to_str(item['url'])

        result['download_data']['parsed_data'][
            'weather_info'] = item['weather_info']
        result['download_data']['parsed_data'][
            'city_info'] = item['city_info']
        with open('{}/{}'.format(result_dir, filename), 'a') as f:
            line = '{}\n'.format(json.dumps(result, ensure_ascii=False))
            f.write(line)

        return item


class MongoDBPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient("mongodb://root:^aTFYU23Aqwe^@10.10.212.209")
        db = client["weather"]
        self.table = db["heweather"]

    def process_item(self, item, spider):
        result = {
            'meta_version': spider.meta_version,
            'meta_updated': datetime.datetime.now().isoformat()[:19],
            'download_config': {
                'url': item["url"],
                'method': 'GET'
            },
            'download_data': {
                'parsed_data': {},
                'raw_data': {},
            }
        }
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, BasicItem):
            try:
                result['download_data']['parsed_data'][
                    'weather_info'] = item['weather_info']
                result['download_data']['parsed_data'][
                    'city_info'] = item['city_info']
                self.table.insert(result)
            except Exception:
                pass
        else:
            raise ValueError("MongoDBPipleline Error")
        return item
