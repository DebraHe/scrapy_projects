# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import datetime

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class LyricPipeline(object):

    def process_item(self, item, spider):
        result_dir = spider.result_dir
        filename = 'lyric.json'
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
        result['download_config']['url'] = item.get('url')
        result['download_data']['parsed_data'][
            'id'] = item.get('id')
        result['download_data']['parsed_data'][
            'raw_lyric'] = item.get('raw_lyric')
        result['download_data']['raw_data'] = item.get('raw_lyric').encode('utf-8')
        with open('{}/{}'.format(result_dir, filename), 'a') as f:
            line = '{}\n'.format(json.dumps(result, ensure_ascii=False))
            f.write(line)


class CommentPipeline(object):

    def process_item(self, item, spider):
        result_dir = spider.result_dir
        filename = 'comment.json'
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
        result['download_config']['url'] = item.get('url')
        result['download_data']['parsed_data'][
            'id'] = item.get('id')
        result['download_data']['parsed_data'][
            'user_name'] = item.get('user_name')
        result['download_data']['parsed_data'][
            'content'] = item.get('content')
        result['download_data']['parsed_data'][
            'com_time'] = item.get('com_time')
        result['download_data']['parsed_data'][
            'praise_num'] = item.get('praise_num')
        with open('{}/{}'.format(result_dir, filename), 'a') as f:
            line = '{}\n'.format(json.dumps(result, ensure_ascii=False))
            f.write(line)
