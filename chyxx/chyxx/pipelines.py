# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import json

import sys

import pymongo

reload(sys)
sys.setdefaultencoding('utf-8')


class ChyxxPipeline(object):
    def process_item(self, item, spider):
        result_dir = spider.result_dir
        filename = spider.filename
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
        result['download_data']['parsed_data']['copyrightHolder'] = item['copyrightHolder'].encode('utf-8')
        result['download_data']['parsed_data']['Bigtype'] = item['Bigtype']
        result['download_data']['parsed_data']['annex'] = item['annex']
        with open('{}/{}'.format(result_dir, filename), 'a') as f:
            line = '{}\n'.format(json.dumps(result, ensure_ascii=False))
            f.write(line)


class MongoDBPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient("mongodb://root:^aTFYU23Aqwe^@10.10.212.209")
        db = client["news"]
        self.table = db["chyxx"]

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

        try:
            result['download_data']['parsed_data']['datePublished'] = item['datePublished'].encode('utf-8')
            result['download_data']['parsed_data']['headline'] = item['headline'].encode('utf-8')
            result['download_data']['parsed_data']['articleBody'] = item['articleBody'].encode('utf-8')
            result['download_data']['parsed_data']['copyrightHolder'] = item['copyrightHolder'].encode('utf-8')
            result['download_data']['parsed_data']['Bigtype'] = item['Bigtype']
            result['download_data']['parsed_data']['annex'] = item['annex']
            self.table.insert(result)
        except Exception:
            pass

        return item

