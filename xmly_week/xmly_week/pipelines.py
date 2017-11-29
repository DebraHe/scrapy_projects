 # -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime

import pymongo
from xmly_week.items import XmlyInfoItem
from xmly_week.items import XmlyDetailItem


class MongoDBPipeline(object):
    def __init__(self):
        client = pymongo.MongoClient("mongodb://root:^aTFYU23Aqwe^@10.10.212.209")
        # client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
        db = client["voice"]
        self.table = db["xmly"]

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
        if isinstance(item, XmlyInfoItem):
            result['download_data']['parsed_data']['title'] = item['title']
            result['download_data']['parsed_data'][
                'cover_pic'] = item['cover_pic']
            result['download_data']['parsed_data'][
                'play_count'] = item['play_count']
            result['download_data']['parsed_data'][
                'first_level'] = item['first_level']
            result['download_data']['parsed_data'][
                'second_level'] = item['second_level']
            result['download_data']['parsed_data'][
                'xmly_uploader_id'] = item['xmly_uploader_id']
            result['download_data']['parsed_data'][
                'xmly_album_id'] = item['xmly_album_id']
            result['download_data']['parsed_data'][
                'last_track'] = item['last_track']
            result['download_data']['parsed_data']['intro'] = item['intro']
            self.table.insert(result)
        elif isinstance(item, XmlyDetailItem):
            result['download_data']['parsed_data'][
                'uploader'] = item['uploader']
            result['download_data']['parsed_data'][
                'uploader_cover'] = item['uploader_cover']
            result['download_data']['parsed_data']['title'] = item['title']
            result['download_data']['parsed_data'][
                'xmly_uploader_id'] = item['xmly_uploader_id']
            result['download_data']['parsed_data'][
                'xmly_album_id'] = item['xmly_album_id']
            result['download_data']['parsed_data'][
                'xmly_sound_id'] = item['xmly_sound_id']
            result['download_data']['parsed_data'][
                'track_play_count'] = item['track_play_count']
            result['download_data']['parsed_data'][
                'track_upload_date'] = item['track_upload_date']
            result['download_data']['parsed_data'][
                'track_title'] = item['track_title']
            result['download_data']['parsed_data'][
                'track_in_album'] = item['track_in_album']
            result['download_data']['parsed_data']['labels'] = item['labels']
            self.table.insert(result)
        else:
            raise ValueError("MongoDBPipleline Error")
        return item