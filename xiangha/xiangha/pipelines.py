# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from xiangha.items import XianghaShicaiItem
import codecs
import json
import datetime
import uuid


class XianghaPipeline(object):

    def process_item(self, item, spider):
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
        if isinstance(item, XianghaShicaiItem):
            filename = "xiangha_full.json"
            result["download_data"]["parsed_data"]["name"] = item["name"]
            result["download_data"]["parsed_data"][
                "description"] = item["description"]
            result["download_data"]["parsed_data"]["富含食材"] = item["food"]
            result["download_data"]["parsed_data"]["@id"] = str(uuid.uuid3(uuid.UUID(
                '0123456789abcdef0123456789abcdef'), 'BinaryRelationOut' + item['url'].encode('utf8')))
            result["download_data"]["parsed_data"]["@type"] = "营养物质"

        with codecs.open('{}/{}'.format(result_dir, filename), 'a', encoding='utf-8') as f:
            line = json.dumps(result) + '\n'
            f.write(line.decode("unicode_escape"))
        return item


class SchemaPipeline(object):
    def process_item(self, item, spider):
        filename = 'result.json'
        result_dir = spider.result_dir

        result = item['schema']

        with open('{}/{}'.format(result_dir, filename), 'a') as f:
            line = '{}\n'.format(json.dumps(result, ensure_ascii=False))
            f.write(line)

        return item
