# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import datetime


class TianyanchaPipeline(object):
    def process_item(self, item, spider):
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
        # 这两个是 str
        result['download_config']['url'] = item['source_url']
        result['download_data']['parsed_data']['kw'] = item['kw']
        # unicode to str
        result['download_data']['parsed_data']['item_url'] = item['item_url'].encode('utf8')
        result['download_data']['parsed_data']['名称'] = item['name'].encode('utf8')
        result['download_data']['parsed_data']['法定代表人'] = item['legal'].encode('utf8')
        result['download_data']['parsed_data']['注册资本'] = item['capital'].encode('utf8')
        result['download_data']['parsed_data']['注册时间'] = item['registration_date'].encode('utf8')
        result['download_data']['parsed_data']['企业状态'] = item['status'].encode('utf8')
        result['download_data']['parsed_data']['省份'] = item['province'].encode('utf8')

        filename = 'tianyancha_list.json'
        with open('{}/{}'.format(result_dir, filename), 'a') as f:
            line = '{}\n'.format(json.dumps(result, ensure_ascii=False))
            f.write(line)
        return item


class TianyanchaDetailPipeline(object):
    def process_item(self, item, spider):
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
        if item['source_url']:
            result['download_config']['url'] = item['source_url']
        else:
            result['download_config']['url'] = ''
        if item['name']:
            result['download_data']['parsed_data']['名称'] = item['name'].encode('utf8')
        else:
            result['download_data']['parsed_data']['名称'] = ''
        if item['addr']:
            result['download_data']['parsed_data']['地址'] = item['addr'].encode('utf8')
        else:
            result['download_data']['parsed_data']['地址'] = ''
        if item['phone']:
            result['download_data']['parsed_data']['电话'] = item['phone'].encode('utf8')
        else:
            result['download_data']['parsed_data']['电话'] = ''
        if item['email']:
            result['download_data']['parsed_data']['邮箱'] = item['email'].encode('utf8')
        else:
            result['download_data']['parsed_data']['邮箱'] = ''
        if item['website']:
            result['download_data']['parsed_data']['网址'] = item['website'].encode('utf8')
        else:
            result['download_data']['parsed_data']['网址'] = ''
        if item['reg_id']:
            result['download_data']['parsed_data']['工商注册号'] = item['reg_id'].encode('utf8')
        else:
            result['download_data']['parsed_data']['工商注册号'] = ''
        if item['org_id']:
            result['download_data']['parsed_data']['组织机构代码'] = item['org_id'].encode('utf8')
        else:
            result['download_data']['parsed_data']['组织机构代码'] = ''
        if item['credit_id']:
            result['download_data']['parsed_data']['统一信用代码'] = item['credit_id'].encode('utf8')
        else:
            result['download_data']['parsed_data']['统一信用代码'] = ''
        if item['company_type']:
            result['download_data']['parsed_data']['企业类型'] = item['company_type'].encode('utf8')
        else:
            result['download_data']['parsed_data']['企业类型'] = ''
        if item['taxpayer_id']:
            result['download_data']['parsed_data']['纳税人识别号'] = item['taxpayer_id'].encode('utf8')
        else:
            result['download_data']['parsed_data']['纳税人识别号'] = ''
        if item['industry']:
            result['download_data']['parsed_data']['行业'] = item['industry'].encode('utf8')
        else:
            result['download_data']['parsed_data']['行业'] = ''
        if item['expiry']:
            result['download_data']['parsed_data']['营业期限'] = item['expiry'].encode('utf8')
        else:
            result['download_data']['parsed_data']['营业期限'] = ''
        if item['check_date']:
            result['download_data']['parsed_data']['核准日期'] = item['check_date'].encode('utf8')
        else:
            result['download_data']['parsed_data']['核准日期'] = ''
        if item['reg_org']:
            result['download_data']['parsed_data']['登记机关'] = item['reg_org'].encode('utf8')
        else:
            result['download_data']['parsed_data']['登记机关'] = ''
        if item['reg_addr']:
            result['download_data']['parsed_data']['注册地址'] = item['reg_addr'].encode('utf8')
        else:
            result['download_data']['parsed_data']['注册地址'] = ''
        if item['scope']:
            result['download_data']['parsed_data']['经营范围'] = item['scope'].encode('utf8')
        else:
            result['download_data']['parsed_data']['经营范围'] = ''
        if item['score']:
            result['download_data']['parsed_data']['评分'] = item['score'].encode('utf8')
        else:
            result['download_data']['parsed_data']['评分'] = ''

        if item['staff_people']:
            result['download_data']['parsed_data']['主要人员'] = item['staff_people']
        else:
            result['download_data']['parsed_data']['主要人员'] = []
        if item['invest']:
            result['download_data']['parsed_data']['对外投资'] = item['invest']
        else:
            result['download_data']['parsed_data']['对外投资'] = []



        if item['gudong']:
            result['download_data']['parsed_data']['股东信息'] = item['gudong']
        else:
            result['download_data']['parsed_data']['股东信息'] = []

        # if item['biangeng']:
        #     result['download_data']['parsed_data']['变更记录'] = item['biangeng']
        # else:
        #     result['download_data']['parsed_data']['变更记录'] = []
        #
        # if item['rongzi']:
        #     result['download_data']['parsed_data']['融资历史'] = item['rongzi']
        # else:
        #     result['download_data']['parsed_data']['融资历史'] = []
        #
        # if item['team_member']:
        #     result['download_data']['parsed_data']['核心团队'] = item['team_member']
        # else:
        #     result['download_data']['parsed_data']['核心团队'] = []
        #
        # if item['firmProduct']:
        #     result['download_data']['parsed_data']['企业业务'] = item['firmProduct']
        # else:
        #     result['download_data']['parsed_data']['企业业务'] = []
        #
        # if item['touzi_event']:
        #     result['download_data']['parsed_data']['投资事件'] = item['touzi_event']
        # else:
        #     result['download_data']['parsed_data']['投资事件'] = []
        #
        # if item['lawsuit']:
        #     result['download_data']['parsed_data']['法律诉讼'] = item['lawsuit']
        # else:
        #     result['download_data']['parsed_data']['法律诉讼'] = []
        #
        # if item['jingpin']:
        #     result['download_data']['parsed_data']['竞品信息'] = item['jingpin']
        # else:
        #     result['download_data']['parsed_data']['竞品信息'] = []
        #
        # if item['court']:
        #     result['download_data']['parsed_data']['法院公告'] = item['court']
        # else:
        #     result['download_data']['parsed_data']['法院公告'] = []
        #
        # if item['zhixing']:
        #     result['download_data']['parsed_data']['被执行人'] = item['zhixing']
        # else:
        #     result['download_data']['parsed_data']['被执行人'] = []
        #
        # if item['announcementcourt']:
        #     result['download_data']['parsed_data']['行政处罚'] = item['announcementcourt']
        # else:
        #     result['download_data']['parsed_data']['行政处罚'] = []
        #
        # if item['equity']:
        #     result['download_data']['parsed_data']['股权出质'] = item['equity']
        # else:
        #     result['download_data']['parsed_data']['股权出质'] = []
        #
        # if item['bid']:
        #     result['download_data']['parsed_data']['招投标'] = item['bid']
        # else:
        #     result['download_data']['parsed_data']['招投标'] = []
        #
        # if item['recruit']:
        #     result['download_data']['parsed_data']['招聘'] = item['recruit']
        # else:
        #     result['download_data']['parsed_data']['招聘'] = []
        #
        # if item['taxcredit']:
        #     result['download_data']['parsed_data']['税务评级'] = item['taxcredit']
        # else:
        #     result['download_data']['parsed_data']['税务评级'] = []
        #
        # if item['check']:
        #     result['download_data']['parsed_data']['抽查检查'] = item['check']
        # else:
        #     result['download_data']['parsed_data']['抽查检查'] = []
        #
        # if item['product_info']:
        #     result['download_data']['parsed_data']['产品信息'] = item['product_info']
        # else:
        #     result['download_data']['parsed_data']['产品信息'] = []
        #
        # if item['certificate']:
        #     result['download_data']['parsed_data']['资质证书'] = item['certificate']
        # else:
        #     result['download_data']['parsed_data']['资质证书'] = []
        #
        # if item['wechat']:
        #     result['download_data']['parsed_data']['微信公众号信息'] = item['wechat']
        # else:
        #     result['download_data']['parsed_data']['微信公众号信息'] = []
        #
        # if item['tmInfo']:
        #     result['download_data']['parsed_data']['商标信息'] = item['tmInfo']
        # else:
        #     result['download_data']['parsed_data']['商标信息'] = []
        #
        # if item['patent']:
        #     result['download_data']['parsed_data']['专利信息'] = item['patent']
        # else:
        #     result['download_data']['parsed_data']['专利信息'] = []
        #
        # if item['copyright']:
        #     result['download_data']['parsed_data']['软件著作权'] = item['copyright']
        # else:
        #     result['download_data']['parsed_data']['软件著作权'] = []
        #
        # if item['copyrightWorks']:
        #     result['download_data']['parsed_data']['作品著作权'] = item['copyrightWorks']
        # else:
        #     result['download_data']['parsed_data']['作品著作权'] = []
        #
        # if item['icp']:
        #     result['download_data']['parsed_data']['网站备案'] = item['icp']
        # else:
        #     result['download_data']['parsed_data']['网站备案'] = []

        result['download_config']['员工人数'] = ''
        filename = 'tianyancha_detail.json'
        with open('{}/{}'.format(result_dir, filename), 'a') as f:
            line = '{}\n'.format(json.dumps(result, ensure_ascii=False))
            f.write(line)
        return item
