# -*- coding:utf-8 -*-
import codecs
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

not_matched_file = 'not_matched.txt'
other_info_file = 'other_info.txt'

not_matched_list = []
other_info_dict = {}
with open(not_matched_file) as f:
    for line in f.readlines():
        not_matched_list.append(line.strip())

with open(other_info_file) as f:
    for line in f.readlines():
        other_info_dict[line.strip()] = 1

ret = {}
for target in not_matched_list:
    result_list = []
    for result in other_info_dict:
        if target in result:
            result_list.append(result.decode('utf-8'))
    if result_list:
        s = ", ".join(i.encode('utf8') for i in result_list)
        m = u'{},{}'.format(target, s).encode('utf8')
    ret[u'{}'.format(target)] = u'{},{}'.format(target, s).encode('utf8')
with codecs.open('result/result.csv', 'w') as f:
    f.write('\n'.join(ret.values()))
# print json.dumps(not_matched_list, encoding='UTF-8', ensure_ascii=False)
# print json.dumps(other_info_dict, encoding='UTF-8', ensure_ascii=False)