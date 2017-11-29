# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json

import pymongo
import datetime
from encvs.items import EncvsItem
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class EncvsPipeline(object):
    def process_item(self, item, spider):
        filename = spider.filename
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
        result['download_data']['parsed_data']['headline'] = item['title']
        result['download_data']['parsed_data']['datePublished'] = item['release_time']
        result['download_data']['parsed_data']['copyrightHolder'] = item['source']
        result['download_data']['parsed_data']['articleBody'] = item['content']
        result['download_data']['parsed_data']['enclosure'] = item['enclosure']

        with open('{}/{}'.format(result_dir, filename), 'a') as f:
            line = '{}\n'.format(json.dumps(result, ensure_ascii=False))
            f.write(line)

        return item


class xxfb_MongoDBPipleline(object):
    def __init__(self):
        client = pymongo.MongoClient("mongodb://root:^aTFYU23Aqwe^@10.10.212.209")
        # client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
        db = client["news"]
        self.table = db["xxfb_add"]

    def process_item(self, item, spider):
        for key, val in item.iteritems():
            if isinstance(val, unicode):
                item[key] = val.encode('utf-8')
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
        if isinstance(item, EncvsItem):
            result['download_data']['parsed_data'][u'标题'] = item['title']
            result['download_data']['parsed_data'][u'发布时间'] = item['release_time']
            result['download_data']['parsed_data'][u'发布来源'] = item['source']
            result['download_data']['parsed_data'][u'正文'] = item['content']
            result['download_data']['parsed_data'][u'附件'] = item['enclosure']
            self.table.insert(result)
        return item


class gzdt_MongoDBPipleline(object):
    def __init__(self):
        client = pymongo.MongoClient("mongodb://root:^aTFYU23Aqwe^@10.10.212.209")
        # client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
        db = client["news"]
        self.table = db["gzdt_add"]

    def process_item(self, item, spider):
        for key, val in item.iteritems():
            if isinstance(val, unicode):
                item[key] = val.encode('utf-8')
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
        if isinstance(item, EncvsItem):
            result['download_data']['parsed_data'][u'标题'] = item['title']
            result['download_data']['parsed_data'][u'发布时间'] = item['release_time']
            result['download_data']['parsed_data'][u'发布来源'] = item['source']
            result['download_data']['parsed_data'][u'正文'] = item['content']
            result['download_data']['parsed_data'][u'附件'] = item['enclosure']
            self.table.insert(result)
        return item
