# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import json

import pymongo

from qinbing.items import QinbingItem


class Qinbing_jidan_Pipeline(object):
    def process_item(self, item, spider):
        result_dir = spider.result_dir
        result = {
            'meta_version': spider.meta_version,
            'meta_updated': datetime.datetime.now().isoformat()[:19],
            'download_config': {
                'url': item['url'],
                'method': 'GET',
            },
            'download_data': {
                'parsed_data': {},
                'raw_data': {},
            }
        }
        result['download_data']['parsed_data']['priceValidUntil'] = item['priceValidUntil']
        result['download_data']['parsed_data']['fromLocation'] = item['fromLocation'].encode('utf-8')
        result['download_data']['parsed_data']['price'] = item['price'].encode('utf-8')

        filename = 'qinbing_jidan.json'
        with open('{}/{}'.format(result_dir, filename), 'a') as f:
            line = '{}\n'.format(json.dumps(result, ensure_ascii=False))
            f.write(line)


class Qinbing_news_Pipeline(object):
    def process_item(self, item, spider):
        result_dir = spider.result_dir
        result = {
            'meta_version': spider.meta_version,
            'meta_updated': datetime.datetime.now().isoformat()[:19],
            'download_config': {
                'url': item['url'],
                'method': 'GET',
            },
            'download_data': {
                'parsed_data': {},
                'raw_data': {},
            }
        }
        result['download_data']['parsed_data']['datePublished'] = item['datePublished'].encode('utf-8')
        result['download_data']['parsed_data']['headline'] = item['headline'].encode('utf-8')
        result['download_data']['parsed_data']['articleBody'] = item['articleBody'].encode('utf-8')
        result['download_data']['parsed_data']['news_type'] = item['news_type']

        filename = 'qinbing_news.json'
        with open('{}/{}'.format(result_dir, filename), 'a') as f:
            line = '{}\n'.format(json.dumps(result, ensure_ascii=False))
            f.write(line)


class Qinbing_jidan_MongoDBPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient("mongodb://root:^aTFYU23Aqwe^@10.10.212.209")
        db = client["price"]
        self.table = db["qinbing_jidan"]

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
        if isinstance(item, QinbingItem):
            try:
                result['download_data']['parsed_data']['priceValidUntil'] = item['priceValidUntil']
                result['download_data']['parsed_data']['fromLocation'] = item['fromLocation'].encode('utf-8')
                result['download_data']['parsed_data']['price'] = item['price'].encode('utf-8')
                self.table.insert(result)
            except Exception:
                pass
        else:
            raise ValueError("MongoDBPipleline Error")
        return item


class Qinbing_news_MongoDBPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient("mongodb://root:^aTFYU23Aqwe^@10.10.212.209")
        db = client["news"]
        self.table = db["qinbing"]

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
        if isinstance(item, QinbingItem):
            try:
                result['download_data']['parsed_data']['datePublished'] = item['datePublished'].encode('utf-8')
                result['download_data']['parsed_data']['headline'] = item['headline'].encode('utf-8')
                result['download_data']['parsed_data']['articleBody'] = item['articleBody'].encode('utf-8')
                result['download_data']['parsed_data']['news_type'] = item['news_type']
                self.table.insert(result)
            except Exception:
                pass
        else:
            raise ValueError("MongoDBPipleline Error")
        return item

