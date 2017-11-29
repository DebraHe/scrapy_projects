# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import datetime
from qingting.items import QingtingDetailItem


class MongoDBPipleline(object):
    def __init__(self):
        client = pymongo.MongoClient("mongodb://root:^aTFYU23Aqwe^@10.10.212.209")
        # client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
        db = client["voice"]
        self.table = db["qingting"]

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
        if isinstance(item, QingtingDetailItem):
            result['download_data']['parsed_data']['title'] = item['title']
            result['download_data']['parsed_data']['qingting_channel_id'] = item['qingting_channel_id']
            result['download_data']['parsed_data']['qingting_programs_id'] = item['qingting_programs_id']
            result['download_data']['parsed_data']['tracks'] = item['tracks']
            result['download_data']['parsed_data']['track_title'] = item['track_title']
            result['download_data']['parsed_data']['play_time'] = item['play_time']
            result['download_data']['parsed_data']['play_count'] = item['play_count']
            result['download_data']['parsed_data']['update_time'] = item['update_time']
            result['download_data']['parsed_data']['last_update'] = item['last_update']
            result['download_data']['parsed_data']['anchor_cover_pic'] = item['anchor_cover_pic']
            result['download_data']['parsed_data']['anchor_name'] = item['anchor_name']
            result['download_data']['raw_data']['mediainfo'] = item['mediainfo']
            self.table.insert(result)
        return item
