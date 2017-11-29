# -*- coding: utf-8 -*-
import codecs
import json

import re

RESULT_FILE = 'person.json'
req = {}
ret_accurate = {}
ret_not_accurate = {}
with codecs.open('people-fromhu.txt', encoding='utf-8') as f:
    for line in f.readlines():
        poet_name = line.strip().split(u'\t')[0]
        # if poet_name not in req:
        req[poet_name] = 1
        # else:
        #     req[poet_name] = req[poet_name] + 1

with open(RESULT_FILE) as f:
    for line in f.readlines():
        try:
            name = json.loads(line.strip()).get('name')
            keywords = json.loads(line.strip()).get('keywords')
            occupation = json.loads(line.strip()).get('occupation')
            if not keywords:
                keywords = []
            if not occupation:
                occupation = ""
            description = json.loads(line.strip()).get('description')
            if name in req:
                if u'诗人' in keywords or u'诗人' in occupation:
                    ret_accurate[name] = u'{},{}'.format(name, description).encode('utf8')
                else:
                    ret_not_accurate[name] = u'{},{}'.format(name, description).encode('utf8')
        except:
            print 'error {}'.format(line)
            continue
with codecs.open('person_desc.csv', 'w') as f_write:
    f_write.write('\n'.join(ret_accurate.values()))
with codecs.open('person_desc_not_accurate.csv', 'w') as f_write:
    f_write.write('\n'.join(ret_not_accurate.values()))

print len(req)
print len(ret_accurate)
print len(ret_not_accurate)
for item in req:
    if item not in ret_accurate and item not in ret_not_accurate:
        print item

