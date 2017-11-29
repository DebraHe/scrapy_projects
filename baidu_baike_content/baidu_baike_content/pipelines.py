# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import datetime
import json

from tool.tool import unicode_to_str


class BaiduBaikeContentPipeline(object):
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
        result['download_config']['url'] = unicode_to_str(item['raw_url'])

        result['download_data']['raw_data'][
            'raw_page_content'] = unicode_to_str(item['raw_page_content'])
        result['download_data']['raw_data'][
            'raw_url'] = unicode_to_str(item['raw_url'])
        result['download_data']['raw_data'][
            'raw_kw'] = unicode_to_str(item['raw_kw'])
        result['download_data']['raw_data'][
            'raw_type'] = unicode_to_str(item['raw_type'])
        result['download_data']['raw_data'][
            'raw_main'] = unicode_to_str(item['raw_main'])

        result['download_data']['raw_data'][
            'raw_kw_type'] = unicode_to_str(item['raw_kw_type'])

        with open('{}/{}'.format(result_dir, filename), 'a') as f:
            line = '{}\n'.format(json.dumps(result, ensure_ascii=False))
            f.write(line)
        with codecs.open('doc/done.txt', 'a', encoding='utf-8') as f:
            f.write(result['download_data']['raw_data']
                    ['raw_kw'] + '\n')
        return item


class BaiduBaikeDoubanPipeline(object):
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
        result['download_config']['url'] = unicode_to_str(item['raw_url'])

        result['download_data']['raw_data'][
            'raw_page_content'] = unicode_to_str(item['raw_page_content'])
        result['download_data']['raw_data'][
            'raw_url'] = unicode_to_str(item['raw_url'])
        result['download_data']['raw_data'][
            'raw_kw'] = unicode_to_str(item['raw_kw'])
        result['download_data']['raw_data'][
            'raw_type'] = unicode_to_str(item['raw_type'])
        result['download_data']['raw_data'][
            'raw_main'] = unicode_to_str(item['raw_main'])

        result['download_data']['raw_data'][
            'raw_douban_id'] = unicode_to_str(item['raw_douban_id'])

        with open('{}/{}'.format(result_dir, filename), 'a') as f:
            line = '{}\n'.format(json.dumps(result, ensure_ascii=False))
            f.write(line)
        with codecs.open('doc/done.txt', 'a', encoding='utf-8') as f:
            f.write(result['download_data']['raw_data']
                    ['raw_douban_id'] + '\n')
        return item