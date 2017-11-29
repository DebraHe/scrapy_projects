# -*- coding: utf-8 -*-
import hashlib
import uuid
import time
import hmac
import base64


def get_nonce():
    return str(uuid.uuid1())


def get_timestamp():
    return str(int(time.time()))


def get_signature(msg):
    service_key = "xxx"
    sign = hmac.new(service_key, base64.b64encode(msg) , hashlib.sha1).digest()
    return hashlib.md5(sign).hexdigest()
