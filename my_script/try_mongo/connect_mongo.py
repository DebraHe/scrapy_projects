# -*- coding:utf-8 -*-
import pymongo

client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
db = client["voice"]
table1 = db["qingting"]
# table1.drop()
# table1 = db["idaddy"]
# table1 = db["xmly"]
# table1 = db["qingting"]
# for i in range(10):
# table1.insert({"1": "1"})
# print table1.replace_one({"1": "1"}, {"1": "1", "2":"2"})
# table1.update_one()
print table1.count()
# table1.drop()
# print table1.count()