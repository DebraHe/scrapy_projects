# -*- coding: utf-8 -*-
import pymongo
from pymongo import MongoClient

client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
db = client.a
print db.xxfb_add.find_one()