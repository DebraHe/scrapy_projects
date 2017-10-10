# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
from tool.tool import unicode_to_str
import json
import codecs


class WordSolitairePipeline(object):

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
            'word'] = unicode_to_str(item['word'])
        result['download_data']['parsed_data'][
            'pinyin'] = unicode_to_str(item['pinyin'])
        result['download_data']['parsed_data'][
            'expression'] = unicode_to_str(item['expression'])

        with open('{}/{}'.format(result_dir, filename), 'a') as f:
            line = '{}\n'.format(json.dumps(result, ensure_ascii=False))
            f.write(line)

        with codecs.open('doc/one.txt', 'a', encoding='utf-8') as f:
            f.write(result['download_data']['parsed_data']
                    ['word'] + '\n')

        return item
