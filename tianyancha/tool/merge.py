# -*- coding:utf-8 -*-

import sys
import os
import json

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def merge(file1, file2):
    ret = []
    urls = {}
    with open(file1) as f:
        list_data = [json.loads(item.strip()) for item in f.readlines()]
        l = {}
        for item in list_data:
            k = item.get('download_data').get('parsed_data').get('item_url')
            l[k] = item
    with open(file2) as f:
        datail_data = [json.loads(item.strip()) for item in f.readlines()]
        d = {}
        for item in datail_data:
            k = item.get('download_config').get('url')
            d[k] = item
    result = {
        'meta_version': '',
        'meta_updated': '',
        'download_config': {},
        'download_data': {
            'parsed_data': {'简介':{},'基本信息':{}},
            'raw_data': {},
        }
    }
    print len(set(l.keys())), len(set(d.keys()))
    for k in list(set(l.keys()) & set(d.keys())):
        result['meta_version'] = d[k]['meta_version'].encode('utf-8')
        result['meta_updated'] = d[k]['meta_updated'].encode('utf-8')
        result['download_config']['method'] = d[k]['download_config']['method'].encode('utf-8')
        result['download_config']['url'] = d[k]['download_config']['url'].encode('utf-8')
        result['download_data']['parsed_data'] = dict(d[k]['download_data']['parsed_data'].items()+l[k]['download_data']['parsed_data'].items())
        # result['download_data']['parsed_data']['简介']['名称'] = d[k]['download_data']['parsed_data'][u'名称'].encode('utf-8')
        # result['download_data']['parsed_data']['简介']['地址'] = d[k]['download_data']['parsed_data'][u'地址'].encode('utf-8').replace('地址：','')
        # result['download_data']['parsed_data']['简介']['电话'] = d[k]['download_data']['parsed_data'][u'电话'].encode('utf-8')
        # result['download_data']['parsed_data']['简介']['邮箱'] = d[k]['download_data']['parsed_data'][u'邮箱'].encode('utf-8')
        # result['download_data']['parsed_data']['简介']['网址'] = d[k]['download_data']['parsed_data'][u'网址'].encode('utf-8')
        # result['download_data']['parsed_data']['基本信息']['工商注册号'] = d[k]['download_data']['parsed_data'][u'工商注册号'].encode('utf-8')
        # result['download_data']['parsed_data']['基本信息']['组织机构代码'] = d[k]['download_data']['parsed_data'][u'组织机构代码'].encode('utf-8')
        # result['download_data']['parsed_data']['基本信息']['统一信用代码'] = d[k]['download_data']['parsed_data'][u'统一信用代码'].encode('utf-8')
        # result['download_data']['parsed_data']['基本信息']['企业类型'] = d[k]['download_data']['parsed_data'][u'企业类型'].encode('utf-8')
        # result['download_data']['parsed_data']['基本信息']['纳税人识别号'] = d[k]['download_data']['parsed_data'][u'纳税人识别号'].encode('utf-8')
        # result['download_data']['parsed_data']['基本信息']['行业'] = d[k]['download_data']['parsed_data'][u'行业'].encode('utf-8')
        # result['download_data']['parsed_data']['基本信息']['营业期限'] = d[k]['download_data']['parsed_data'][u'营业期限'].encode('utf-8').replace('\n                            ','')
        # result['download_data']['parsed_data']['基本信息']['核准日期'] = d[k]['download_data']['parsed_data'][u'核准日期'].encode('utf-8')
        # result['download_data']['parsed_data']['基本信息']['登记机关'] = d[k]['download_data']['parsed_data'][u'登记机关'].encode('utf-8')
        # result['download_data']['parsed_data']['基本信息']['注册地址'] = d[k]['download_data']['parsed_data'][u'注册地址'].encode('utf-8')
        # result['download_data']['parsed_data']['基本信息']['经营范围'] = d[k]['download_data']['parsed_data'][u'经营范围'].encode('utf-8')
        # result['download_data']['parsed_data']['基本信息']['评分'] = d[k]['download_data']['parsed_data'][u'评分'].encode('utf-8')
        # result['download_data']['parsed_data']['基本信息']['主要人员'] = d[k]['download_data']['parsed_data'][u'主要人员']
        # result['download_data']['parsed_data']['基本信息']['对外投资'] = d[k]['download_data']['parsed_data'][u'对外投资']
        # result['download_data']['parsed_data']['基本信息']['股东信息'] = d[k]['download_data']['parsed_data'][u'股东信息']
        #
        # # result['download_data']['parsed_data']['基本信息']['变更记录'] = d[k]['download_data']['parsed_data'][u'变更记录']
        # # result['download_data']['parsed_data']['基本信息']['融资历史'] = d[k]['download_data']['parsed_data'][u'融资历史']
        # # result['download_data']['parsed_data']['基本信息']['核心团队'] = d[k]['download_data']['parsed_data'][u'核心团队']
        # # result['download_data']['parsed_data']['基本信息']['企业业务'] = d[k]['download_data']['parsed_data'][u'企业业务']
        # # result['download_data']['parsed_data']['基本信息']['投资事件'] = d[k]['download_data']['parsed_data'][u'投资事件']
        # # result['download_data']['parsed_data']['基本信息']['法律诉讼'] = d[k]['download_data']['parsed_data'][u'法律诉讼']
        # # result['download_data']['parsed_data']['基本信息']['竞品信息'] = d[k]['download_data']['parsed_data'][u'竞品信息']
        # # result['download_data']['parsed_data']['基本信息']['法院公告'] = d[k]['download_data']['parsed_data'][u'法院公告']
        # # result['download_data']['parsed_data']['基本信息']['被执行人'] = d[k]['download_data']['parsed_data'][u'被执行人']
        # # result['download_data']['parsed_data']['基本信息']['行政处罚'] = d[k]['download_data']['parsed_data'][u'行政处罚']
        # # result['download_data']['parsed_data']['基本信息']['股权出质'] = d[k]['download_data']['parsed_data'][u'股权出质']
        # # result['download_data']['parsed_data']['基本信息']['招投标'] = d[k]['download_data']['parsed_data'][u'招投标']
        # # result['download_data']['parsed_data']['基本信息']['招聘'] = d[k]['download_data']['parsed_data'][u'招聘']
        # # result['download_data']['parsed_data']['基本信息']['税务评级'] = d[k]['download_data']['parsed_data'][u'税务评级']
        # # result['download_data']['parsed_data']['基本信息']['抽查检查'] = d[k]['download_data']['parsed_data'][u'抽查检查']
        # # result['download_data']['parsed_data']['基本信息']['产品信息'] = d[k]['download_data']['parsed_data'][u'产品信息']
        # # result['download_data']['parsed_data']['基本信息']['资质证书'] = d[k]['download_data']['parsed_data'][u'资质证书']
        # # result['download_data']['parsed_data']['基本信息']['微信公众号信息'] = d[k]['download_data']['parsed_data'][u'微信公众号信息']
        # # result['download_data']['parsed_data']['基本信息']['商标信息'] = d[k]['download_data']['parsed_data'][u'商标信息']
        # # result['download_data']['parsed_data']['基本信息']['专利信息'] = d[k]['download_data']['parsed_data'][u'专利信息']
        # # result['download_data']['parsed_data']['基本信息']['软件著作权'] = d[k]['download_data']['parsed_data'][u'软件著作权']
        # # result['download_data']['parsed_data']['基本信息']['作品著作权'] = d[k]['download_data']['parsed_data'][u'作品著作权']
        # # result['download_data']['parsed_data']['基本信息']['网站备案'] = d[k]['download_data']['parsed_data'][u'网站备案']
        #
        # result['download_data']['parsed_data']['基本信息']['员工人数'] = ''
        # result['download_data']['parsed_data']['基本信息']['法人信息'] = l[k]['download_data']['parsed_data'][u'法定代表人'].encode('utf-8')
        # result['download_data']['parsed_data']['基本信息']['注册资本'] = l[k]['download_data']['parsed_data'][u'注册资本'].encode('utf-8')
        # result['download_data']['parsed_data']['基本信息']['注册时间'] = l[k]['download_data']['parsed_data'][u'注册时间'].encode('utf-8')
        # result['download_data']['parsed_data']['基本信息']['企业状态'] = l[k]['download_data']['parsed_data'][u'企业状态'].encode('utf-8')

        try:
            with open('tianyancha.json','a') as f:
                s = json.dumps(result,ensure_ascii=False)
                f.write(s+'\n')
        except UnicodeEncodeError as e:
            print result
            break
        else:
            pass


if __name__ == '__main__':
    # try:
    file1 = '../result/tianyancha_list.json'
    file2 = '../result/tianyancha_detail.json'
    merge(file1, file2)
    # except:
    #     print 'python file_merge PATH_TO_RESULT_DIR PATH_TO_MERGED_DIR'
