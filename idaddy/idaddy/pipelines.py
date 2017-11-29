# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import datetime

import pymongo

from idaddy.items import IdaddyDetailItem


class MongoDBPipeline(object):
    def __init__(self):
        # client = pymongo.MongoClient("mongodb://root:^aTFYU23Aqwe^@10.10.212.209")
        client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
        db = client["voice"]
        self.table = db["idaddy"]

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
        if isinstance(item, IdaddyDetailItem):
            try:
                result["download_data"]["parsed_data"]['title'] = item['title']
                result["download_data"]["parsed_data"]['album_id'] = item['album_id']
                result["download_data"]["parsed_data"]['chapter_id'] = item['chapter_id']
                result["download_data"]["parsed_data"][
                    'track_in_albun'] = item['track_in_albun']
                result["download_data"]["parsed_data"][
                    'track_title'] = item['track_title']
                result["download_data"]["parsed_data"][
                    'play_time'] = item['play_time']
                result["download_data"]["parsed_data"][
                    'episodes'] = item['episodes']
                result["download_data"]["parsed_data"]['intro'] = item['intro']
                result["download_data"]["parsed_data"][
                    'rating_number'] = item['rating_number']
                result["download_data"]["parsed_data"]['Type'] = item['Type']
                result["download_data"]["parsed_data"]['cats'] = item['cats']
                self.table.insert(result)
            except Exception:
                pass
        else:
            raise ValueError("MongoDBPipleline Error")
        return item