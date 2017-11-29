# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class CanRkPipeline(object):
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
        result['download_data']['raw_data'] = dict(item)
        result['download_data']['parsed_data']['被执行人姓名/名称'] = item['pname']
        result['download_data']['parsed_data']['身份证号码/组织机构代码'] = item['partyCardNum']
        result['download_data']['parsed_data']['执行法院'] = item['execCourtName']
        result['download_data']['parsed_data']['立案时间'] = item['caseCreateTime']
        result['download_data']['parsed_data']['案号'] = item['caseCode']
        result['download_data']['parsed_data']['执行标的'] = item['execMoney']

        filename = 'zhixing.json'
        with open('{}/{}'.format(result_dir, filename), 'a') as f:
            line = '{}\n'.format(json.dumps(result, ensure_ascii=False))
            f.write(line)
        return item


class CanRk_shixin_Pipeline(object):
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
        result['download_data']['raw_data'] = dict(item)
        result['download_data']['parsed_data']['被执行人姓名/名称'] = item['iname']
        result['download_data']['parsed_data']['性别'] = item['sexy']
        result['download_data']['parsed_data']['年龄'] = item['age']
        result['download_data']['parsed_data']['身份证号码/组织机构代码'] = item['cardNum']
        result['download_data']['parsed_data']['执行法院'] = item['courtName']
        result['download_data']['parsed_data']['省份'] = item['areaName']
        result['download_data']['parsed_data']['执行依据文号'] = item['gistId']
        result['download_data']['parsed_data']['立案时间'] = item['regDate']
        result['download_data']['parsed_data']['案号'] = item['caseCode']
        result['download_data']['parsed_data']['做出执行依据单位'] = item['gistUnit']
        result['download_data']['parsed_data']['生效法律文书确定的义务'] = item['duty']
        result['download_data']['parsed_data']['被执行人的履行情况'] = item['performance']
        result['download_data']['parsed_data']['失信被执行人行为具体情形'] = item['disruptTypeName']
        result['download_data']['parsed_data']['发布时间'] = item['publishDate']
        filename = 'shixin.json'
        with open('{}/{}'.format(result_dir, filename), 'a') as f:
            line = '{}\n'.format(json.dumps(result, ensure_ascii=False))
            f.write(line)
        return item


class CanRk_wenshu_Pipeline(object):
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
        result['download_data']['raw_data'] = item['raw_data']
        result['download_data']['parsed_data']['id'] = item['id']
        result['download_data']['parsed_data']['name'] = item['name']
        result['download_data']['parsed_data']['time'] = item['time']
        result['download_data']['parsed_data']['kw'] = item['kw']

        filename = 'wenshu.json'
        with open('{}/{}'.format(result_dir, filename), 'a') as f:
            line = '{}\n'.format(json.dumps(result, ensure_ascii=False))
            f.write(line)
        return item


class CanRk_wenshu_detail_Pipeline(object):
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
        result['download_data']['raw_data'] = item['raw_data']
        result['download_data']['parsed_data']['id'] = item['id']
        result['download_data']['parsed_data']['content'] = item['content']

        filename = 'wenshu_detail.json'
        with open('{}/{}'.format(result_dir, filename), 'a') as f:
            line = '{}\n'.format(json.dumps(result, ensure_ascii=False))
            f.write(line)
        with open('doc/succeed_wenshu_id.txt', 'a') as f:
            f.write(item['id'] + '\n')
        return item