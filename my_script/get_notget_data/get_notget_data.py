# -*- coding: utf-8 -*-
import codecs
import json
import sys
import uuid

reload(sys)
sys.setdefaultencoding('utf-8')
# over = {}
# with codecs.open('done.txt', 'r', encoding='utf-8') as f1:
#     for line1 in f1.readlines():
#         over[line1.strip()] = 1
#



# result = []
# with open('food_ingredient.json') as f2:
#     for line2 in f2.readlines():
#         page_name = json.loads(line2.strip()).get('name')   # 读取页面HTML
#         if page_name in over:
#             continue
#         with codecs.open('notyet.json', 'a', encoding='utf-8') as f:
#             line = json.dumps(json.loads(line2.strip())) + '\n'
#             f.write(line.decode("unicode_escape"))

#
# with codecs.open('notyet.json', 'r') as f2:
#     for line2 in f2.readlines():
#         line = json.loads(line2.strip(), "UTF-8").get('name')
# #
#         with codecs.open('notyet.txt', 'a', encoding='utf-8') as f:
#             f.write(line + '\n')


# small_type = {}
# global null
# null = ""
# with open('shicai.json') as f2:
#     for line2 in f2.readlines():
#         small_type[eval(line2.strip())['tag'][1]['name']] = eval(line2.strip())['tag'][0]['name']
# for k, v in small_type.items():
#     print v+"   "+k
# print 'xxxxxx'
# for k, v in small_type.items():
#     print k


# over = {}
# with codecs.open('notyet_have_tag.txt', 'r', encoding='utf-8') as f1:
#     for line1 in f1.readlines():
#         names = line1.strip().split(u'\t')
#         shicai_name = names[0]
#         tag_name = names[1:]
#         over[shicai_name] = tag_name
#
# result = []
# global null
# null = ""
# with open('notyet.json') as f2:
#     for line2 in f2.readlines():
#         page_name = json.loads(line2.strip()).get('name')   # 读取页面HTML
#         if page_name in over:
#             item = eval(line2)
#             tags = []
#             for tag in over[page_name]:
#                 tags.append({
#                     "name": tag,
#                     "@id": str(uuid.uuid3(uuid.UUID('0123456789abcdef0123456789abcdef'), "Tag" + tag.encode('utf8'))),
#                     "@type": ["Tag", "Thing"],
#                     "category": "taxonomy"
#                 })
#             item["tag"] = tags
#             with codecs.open('update_data.json', 'a', encoding='utf-8') as f:
#                 line = json.dumps(item, ensure_ascii=False) + '\n'
#                 f.write(line)

global null
null = ""
i = 1
with open('douban_people_parsed.json') as f2:
    for line2 in f2.readlines():
        page_name = json.loads(line2.strip())   # 读取页面HTML

        print i
        i = i + 1