# -*- coding: utf-8 -*-
import sys
import pymongo

reload(sys)
sys.setdefaultencoding('utf-8')

qingting_channel_dict = {}

client = pymongo.MongoClient("mongodb://root:^aTFYU23Aqwe^@10.10.212.209")
db = client["voice"]
table = db["qingting"]
for item in table.find():
        qingting_item = item
        qingting_channel_id = qingting_item.get('download_data').get('parsed_data').get('qingting_channel_id')
        qingting_programs_id = qingting_item.get('download_data').get('parsed_data').get('qingting_programs_id')

        if qingting_channel_id not in qingting_channel_dict:
            qingting_channel_dict[qingting_channel_id] = []
        qingting_channel_dict[qingting_channel_id].append(qingting_item)
for k, v in qingting_channel_dict.items():
    qingting_programs_dict = {}
    for v_item in v:
        qingting_programs_dict[v_item['download_data']['parsed_data']['qingting_programs_id']] = v_item['download_data']['parsed_data']['update_time']
    qingting_programs_dict = sorted(qingting_programs_dict.items(), key=lambda item: item[1], reverse=True)
    for v_item_insert in v:
        index_item = (v_item_insert['download_data']['parsed_data']['qingting_programs_id'], v_item_insert['download_data']['parsed_data']['update_time'])
        if index_item in qingting_programs_dict:
            object_id = v_item_insert.get('_id')
            print table.find_one({'_id': object_id})
            v_item_insert['download_data']['parsed_data']['position'] = qingting_programs_dict.index(index_item) + 1
            table.replace_one({'_id': object_id}, v_item_insert)



