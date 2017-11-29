# -*- coding: utf-8 -*-

import hashlib
import uuid
import time


def get_nonce():
    return str(uuid.uuid1())


def get_timestamp():
    return str(int(time.time()))


def get_signature(app_id, timestamp):
    service_key = "XXX"
    return hashlib.sha1(app_id + service_key + str(timestamp)).hexdigest()
