# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import codecs
import datetime
import os
import pymongo


class MongoDBPipleline(object):

    def __init__(self):
        client = pymongo.MongoClient(
            "mongodb://root:^aTFYU23Aqwe^@10.10.212.209")
        # client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
        self.db = client['news']

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
        table = self.db['weixin_{}'.format(item['kind'])]
        for k in item.keys():
            if k == 'url' or k == 'kind':
                continue
            result['download_data']['parsed_data'][k] = item[k]
        table.insert(result)
        return item


class WeixinPipeline(object):

    def process_item(self, item, spider):
        today = datetime.date.today().strftime('%Y%m%d')
        prefix = 'news'
        filename = '{}_{}_{}all'.format(
            prefix, item['kind'], today) + '.json'
        result_dir = spider.result_dir
        if not os.path.exists(result_dir):
            os.mkdir(result_dir)
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
        for k in item.keys():
            if k == 'url':
                continue
            result['download_data']['parsed_data'][k] = item[k]
        result['download_config']['url'] = item['url']
        with codecs.open('{}/{}'.format(spider.result_dir, filename), 'a', encoding='utf-8') as f:
            line = json.dumps(result, ensure_ascii=False) + '\n'
            f.write(line)
        return item
