# -*- coding: utf-8 -*-

import codecs
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import json

from tool.tool import unicode_to_str


class BasicPipeline(object):
    def process_item(self, item, spider):
        filename = 'result.json'
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
            'kw'] = unicode_to_str(item['kw'])
        result['download_data']['parsed_data'][
            'name'] = unicode_to_str(item['name'])
        result['download_data']['parsed_data'][
            'image_url'] = unicode_to_str(item['image_url'])

        result['download_data']['parsed_data'][
            'info'] = item['info']

        with open('{}/{}'.format(result_dir, filename), 'a') as f:
            line = '{}\n'.format(json.dumps(result, ensure_ascii=False))
            f.write(line)

        with codecs.open('doc/done.txt', 'a', encoding='utf-8') as f:
            f.write(result['download_data']['parsed_data']
                    ['kw'] + '\n')

        return item


class PlacePipeline(object):
    def process_item(self, item, spider):
        filename = 'result.json'
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
            'kw'] = unicode_to_str(item['kw'])
        result['download_data']['parsed_data'][
            'info'] = item['info']

        with open('{}/{}'.format(result_dir, filename), 'a') as f:
            line = '{}\n'.format(json.dumps(result, ensure_ascii=False))
            f.write(line)

        with codecs.open('doc/done.txt', 'a', encoding='utf-8') as f:
            f.write(result['download_data']['parsed_data']
                    ['kw'] + '\n')

        return item
